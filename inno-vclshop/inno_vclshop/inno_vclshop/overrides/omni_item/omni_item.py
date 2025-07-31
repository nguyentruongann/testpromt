import mimetypes
import os

import frappe
import requests
from bs4 import BeautifulSoup, Tag
from frappe import _
from frappe.utils.file_manager import save_file

import json

from inno_erp.inno_omnichannel.doctype.omni_item.omni_item import OmniItem


MAX_FILES_GALLERY = 5
MAX_FILES_VIEW360 = 8

MEDIA_FIELDS = [
		"attach_image_1",
		"attach_image_2",
		"attach_image_3",
		"attach_image_4",
		"attach_image_5",
	]

MEDIA_360_FIELDS = [
	"attach_360_image_1",
	"attach_360_image_2",
	"attach_360_image_3",
	"attach_360_image_4",
	"attach_360_image_5",
	"attach_360_image_6",
	"attach_360_image_7",
	"attach_360_image_8",
]

class VclInnoOmniItem(OmniItem):
	def before_save(self):
		custom_upload_media_change = self.has_value_changed("custom_upload_media")
		custom_upload_media_360_change = self.has_value_changed("custom_upload_media_360")

		if custom_upload_media_change:

			self.populate_attach_images(
				folder_field="custom_upload_media",
				image_fields=MEDIA_FIELDS,
				max_files=MAX_FILES_GALLERY
			)


		if custom_upload_media_360_change:
			self.populate_attach_images(
				folder_field="custom_upload_media_360",
				image_fields=MEDIA_360_FIELDS,
				max_files=MAX_FILES_VIEW360
			)
	def populate_attach_images(self, folder_field, image_fields, max_files):
		try:
			self.clear_attach_images(image_fields)
			self.clear_attachments_from_old_folder(folder_field)
			folder_value = getattr(self, folder_field, None)
			if not folder_value:
				return

			all_files = self.get_all_files_from_folder(folder_value)

			if not all_files:
				return

			files_to_assign = all_files[:max_files]

			for i, file_url in enumerate(files_to_assign):
				if i < len(image_fields):
					setattr(self, image_fields[i], file_url)

		except Exception as e:
			self.clear_attach_images(image_fields)
			frappe.msgprint(
				_(f"Error loading images from folder. Please check the folder selection."),
				indicator="red"
			)
        

	def clear_attach_images(self, image_fields):
		for field in image_fields:
			setattr(self, field, None)

	def is_file_in_folder(self, file_name, folder_name):
		try:
			file_doc = frappe.get_doc("File", file_name)

			folder_ids = [folder_name]

			def get_subfolder_ids(parent_folder):
				subfolders = frappe.get_list("File",
					filters={
						"folder": parent_folder,
						"is_folder": 1
					},
					fields=["name"]
				)
				for subfolder in subfolders:
					folder_ids.append(subfolder.name)
					get_subfolder_ids(subfolder.name)

			get_subfolder_ids(folder_name)

			return file_doc.folder in folder_ids

		except Exception:
			return False

	def clear_attachments_from_old_folder(self, folder_field):
		try:
			old_folder_value = self._doc_before_save.get(folder_field) if hasattr(self, '_doc_before_save') else None

			if not old_folder_value:
				return

			old_folder_files = self.get_all_files_from_folder(old_folder_value)

			if not old_folder_files:
				return

			files_in_folder = frappe.db.get_list('File',
				filters={
					'attached_to_doctype': 'Omni Item',
					'attached_to_name': self.name,
					'file_url': ['in', old_folder_files]
				},
				fields=['name', 'file_url']
			)

			for file_attachment in files_in_folder:
				if self.is_file_in_folder(file_attachment.name, old_folder_value):
					try:
						frappe.db.set_value('File', file_attachment.name, 'attached_to_doctype', None)
						frappe.db.set_value('File', file_attachment.name, 'attached_to_name', None)
					except Exception as e:
						frappe.log_error(frappe.get_traceback(), f"Error unlinking {file_attachment.name}")

			all_item_attachments = frappe.db.get_list('File',
				filters={
					'attached_to_doctype': 'Omni Item',
					'attached_to_name': self.name
				},
				fields=['name', 'file_url']
			)

			for attachment in all_item_attachments:
				if (attachment.file_url in old_folder_files and
					not self.is_file_in_folder(attachment.name, old_folder_value)):
					try:
						frappe.delete_doc("File", attachment.name, force=1)
					except Exception as e:
						frappe.log_error(frappe.get_traceback(), f"Error deleting {attachment.name}")
			frappe.db.commit()
		except Exception as e:
			frappe.log_error(
				frappe.get_traceback(),
				f"Error clearing attachments from old folder for Item {self.name}"
			)


	def get_all_files_from_folder(self, folder_name):
		all_files = []
		try:
			if not folder_name:
				return all_files

			if not frappe.db.exists("File", folder_name):
				return all_files

			folder_doc = frappe.get_doc("File", folder_name)

			if not folder_doc.is_folder:
				return all_files

			children = frappe.get_list("File",
				filters={
					"folder": folder_doc.name
				},
				fields=["name", "file_url", "is_folder", "file_name"],
				order_by="creation asc"
			)

			for child in children:
				if child.is_folder:
					subfolder_files = self.get_all_files_from_folder(child.name)
					all_files.extend(subfolder_files)
				else:
					if child.file_url and self.is_image_file(child.file_name):
						all_files.append(child.file_url)

		except Exception as e:
			frappe.log_error(
				frappe.get_traceback(),
				f"Error getting files from folder {folder_name}"
			)

		return all_files

	def is_image_file(self, filename):
		if not filename:
			return False

		image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'}
		file_extension = filename.lower().split('.')[-1] if '.' in filename else ''
		return f'.{file_extension}' in image_extensions


# ------------------------------Fetch Item from URL--------------------------------
@frappe.whitelist()
def fetch_item_from_url(item_url, item_code=None):
	"""Fetch and update item details from a given URL.

	Args:
	    item_url (str): URL of the item page.
	    item_code (str): Code of the Omni Item document.

	Returns:
	    str: Name of the updated item.
	"""
	if not item_url or not item_code:
		frappe.throw(_("Item Url and Item Code are required"))

	item_data = crawl_item_from_url(item_url, item_code)
	update_omni_item(item_code, item_data)
	return item_code


def crawl_item_from_url(item_url, item_code=None):
	"""Crawl item data from URL and return a dict.

	Args:
	    item_url (str): URL of the item page.
	    item_code (str, optional): Code of the Omni Item document for description images.

	Returns:
	    dict: Extracted item data, parsed soup, and img_urls if item_code is None.
	"""
	html_content = get_html_content(item_url)
	soup = BeautifulSoup(html_content, "lxml")

	description, img_urls = extract_full_description(soup, item_code=item_code)

	item_data = {
		"item_name": get_item_name(soup),
		"brand": get_brand(soup),
		"short_description": extract_short_description(soup),
		"item_specifications": extract_item_specifications(soup),
		"description": description,
		"soup": soup,  # Pass soup for set_images in update
		"img_urls": img_urls if not item_code else [],  # Only include if not attached yet
	}
	return item_data


def update_omni_item(item_code, item_data):
	"""Update Omni Item with crawled data.

	Args:
	    item_code (str): Code of the Omni Item document.
	    item_data (dict): Data from crawl_item_from_url.
	"""
	item = frappe.get_doc("Omni Item", item_code)

	if item.variant_of:
		template_item = frappe.get_doc("Omni Item", item.variant_of)
		if template_item.item_name != template_item.description:
			set_images(item, item_data["soup"])
			print(f"Skipped updating {item_code}, upload images only")
			return
		item = template_item

	# Reset item fields
	# for i in range(1, 6):
	# 	field = f"attach_image_{i}"
	# 	if hasattr(item, field):
	# 		setattr(item, field, None)
	# item.image = None
	# item.short_description = ""
	# item.description = ""
	# item.item_specifications = []
	# item.item_name = ""

	# Assign data from item_data
	# item.item_name = item_data["item_name"]
	# item.brand = item_data["brand"]
	if "Chưa có đánh giá nào." not in item_data["short_description"]:
		item.short_description = item_data["short_description"]
		item.description = item_data["description"]

		# If img_urls present (from crawl without item_code), attach images now and update description
		if item_data.get("img_urls"):
			# Parse the current description to update img src
			soup_desc = BeautifulSoup(item.description, "lxml")
			img_tags = soup_desc.find_all("img")

			for idx, img_url in enumerate(item_data["img_urls"]):
				if idx >= len(img_tags):
					break
				frappe_img_url = download_and_attach_image(img_url, item.doctype, item.name, None)
				if frappe_img_url:
					img_tags[idx]["src"] = frappe_img_url

			# Update description with modified soup
			item.description = soup_desc.decode_contents().strip()

	for spec in item_data["item_specifications"]:
		item.append("item_specifications", spec)

	# Set images using soup from item_data
	set_images(item, item_data["soup"])

	item.save(ignore_permissions=True)


def get_item_name(soup):
	"""Extract item name from soup.

	Args:
	    soup (BeautifulSoup): Parsed HTML soup.

	Returns:
	    str: Item name.
	"""
	title_tag = soup.find("h1", class_="product-title product_title entry-title")
	return title_tag.text.strip() if title_tag else ""


def get_brand(soup):
	"""Extract brand from soup.

	Args:
	    soup (BeautifulSoup): Parsed HTML soup.

	Returns:
	    str: Brand name in uppercase.
	"""
	brand_div = soup.find("div", class_="pwb-single-product-brands pwb-clearfix")

	if not brand_div:
		return

	brand_a = brand_div.find("a")

	if not brand_a:
		return

	if brand_a.find("img"):
		return brand_a["title"].upper()
	else:
		return brand_a.text.strip().upper()


def get_html_content(url):
	"""Fetch HTML content from URL.

	Args:
	    url (str): URL to fetch.

	Returns:
	    str: HTML content.

	Raises:
	    frappe.exceptions.ValidationError: If fetch fails.
	"""
	response = requests.get(url)
	response.raise_for_status()  # Raise error for bad status
	return response.text


def download_and_attach_image(image_url, doctype, docname, fieldname):
	"""Download image and attach to Frappe document.

	Args:
	    image_url (str): URL of the image.
	    doctype (str): Doctype to attach to.
	    docname (str): Docname to attach to.
	    fieldname (str): Field to set.

	Returns:
	    str or None: File URL if successful.
	"""
	try:
		response = requests.get(image_url, timeout=10)
		response.raise_for_status()
		content_type = (
			response.headers.get("Content-Type") or mimetypes.guess_type(image_url)[0] or "image/jpeg"
		)
		ext = mimetypes.guess_extension(content_type) or ".jpg"
		filename = os.path.basename(image_url.split("?")[0])
		if not os.path.splitext(filename)[1]:
			filename += ext
		file_doc = save_file(filename, response.content, doctype, docname, is_private=0, df=fieldname)
		return file_doc.file_url
	except Exception as e:
		frappe.log_error("Failed to download/upload image", e)
		return None


def set_images(item, soup):
	"""Set main and additional images for item.

	Args:
	    item (frappe.Doc): Item document.
	    soup (BeautifulSoup): Parsed HTML soup.
	"""
	image_urls = [
		div.a.get("href")
		for div in soup.find_all(lambda d: d.has_attr("data-thumb"))
		if div.a and div.a.has_attr("href")
	]

	if image_urls:
		# Main image
		frappe_img_url = download_and_attach_image(image_urls[0], item.doctype, item.name, "image")
		if frappe_img_url:
			item.image = frappe_img_url

		# Additional images (up to 8)
		for idx, url in enumerate(image_urls[1:9], start=1):
			fieldname = f"attach_image_{idx}"
			if hasattr(item, fieldname):
				frappe_img_url = download_and_attach_image(url, item.doctype, item.name, fieldname)
				if frappe_img_url:
					setattr(item, fieldname, frappe_img_url)


def extract_short_description(soup):
	"""Extract short description from soup.

	Args:
	    soup (BeautifulSoup): Parsed HTML soup.

	Returns:
	    str: Short description.
	"""
	panel = soup.find("div", class_="panel entry-content")
	if not panel:
		return ""
	gioi_thieu = panel.find("p", class_="gioi-thieu")
	if gioi_thieu:
		return gioi_thieu.text.strip()
	short_div = panel.find("div", class_="product-short-description")
	if short_div and short_div.p:
		return short_div.p.text.strip()
	first_p = panel.find("p")
	if first_p:
		return first_p.text.strip()
	return ""


def extract_item_specifications(soup):
	"""Extract specifications from soup.

	Args:
	    soup (BeautifulSoup): Parsed HTML soup.

	Returns:
	    list: List of spec dicts.
	"""
	specs = []

	# Priority 1: Check for div.hscroll with table
	if hscroll := soup.find("div", class_="hscroll"):
		table = hscroll.find("table")
		if table:
			rows = table.find_all("tr")
			for row in rows:
				cols = row.find_all("td")
				if len(cols) == 2:
					key = cols[0].text.strip()
					value = cols[1].text.strip()
					if len(value) > 140:
						return []
					specs.append({"spec_name": key, "spec_value": value})
		if specs:
			return specs

	# Priority 2: Check for h2 with id starting with 'danhsach-thong-so-ky-thuat' and next ul or p
	elif h2 := soup.find("h2", id=lambda x: x and x.startswith("danhsach-thong-so-ky-thuat")):
		print("Priority 2")
		ul = h2.find_next("ul")
		if ul:
			lis = ul.find_all("li")
			for li in lis:
				if ":" in li.text:
					key, value = li.text.split(":", 1)
					if len(value) > 140:
						return []
					specs.append({"spec_name": key.strip(), "spec_value": value.strip()})
		else:
			p = h2.find_next("p")
			if p:
				# Lấy từng dòng, tách theo <br>
				lines = [line.strip() for line in p.decode_contents().replace("\r", "").split("<br/>")]
				for line in lines:
					# Loại bỏ dấu ngoặc kép đầu/cuối nếu có
					line = line.strip().strip('"').strip("'").lstrip("-–").strip()
					if ":" in line:
						key, value = line.split(":", 1)
						if len(value) > 140:
							return []
						specs.append({"spec_name": key.strip(), "spec_value": value.strip()})
		if specs:
			return specs

	# Priority 3: Check for woocommerce table
	elif woocommerce := soup.find("table", class_="woocommerce-product-attributes shop_attributes"):
		print("Priority 3")
		trs = woocommerce.find_all("tr")
		if trs:
			for tr in trs:
				th = tr.find("th")
				td = tr.find("td")
				if th and td:
					key = th.text.strip()
					value = td.text.strip()
					if len(value) > 140:
						return []
					specs.append({"spec_name": key, "spec_value": value})
		if specs:
			return specs

	# Priority 4: Check for h3 with id and next div siblings
	elif h3 := soup.find("h3", id="danhsach-thong-so-ky-thuat"):
		print("Priority 4")
		sibling = h3.find_next_sibling()
		while sibling:
			if sibling.name == "div":
				text = sibling.get_text(strip=True)
				if ":" in text:
					key, value = text.split(":", 1)
					if len(value) > 140:
						return []
					key = key.replace("–", "").strip()
					specs.append({"spec_name": key, "spec_value": value.strip()})
			elif sibling.name != "div":
				break
			sibling = sibling.find_next_sibling()
		if specs:
			return specs

	# Priority 5: Check for div.rivaki after specific h2
	elif rivakis := soup.find_all("div", class_="rivaki"):
		print("Priority 5")
		target_rivaki = None
		for rivaki in rivakis:
			prev = rivaki.find_previous_sibling()
			while prev:
				if isinstance(prev, Tag) and prev.name == "h2":
					h2_id = prev.get("id", "")
					# Check both variations to handle potential inconsistencies
					if h2_id.startswith("danhsach-thong-so-ki-thuat") or h2_id.startswith(
						"danhsach-thong-so-ky-thuat"
					):
						target_rivaki = rivaki
						break
				prev = prev.previous_sibling
			if target_rivaki:
				break

		if target_rivaki:
			lis = target_rivaki.find_all("li")
			if lis:
				for li in lis:
					if ":" in li.text:
						key, value = li.text.split(":", 1)
						if len(value) > 140:
							return []

						specs.append({"spec_name": key.strip(), "spec_value": value.strip()})
		if specs:
			return specs
	return specs


def extract_full_description(soup, item_code=None):
	"""Extract and clean full description from soup.

	Args:
	    soup (BeautifulSoup): Parsed HTML soup.
	    item_code (str, optional): Code of the Omni Item document for attaching images.

	Returns:
	    tuple: (Cleaned HTML description, list of image URLs if item_code is None)
	"""
	panel = soup.find("div", class_="panel entry-content")
	if not panel:
		return "", []

	# Remove all <a> tags
	for a in panel.find_all("a"):
		a.decompose()

	found = False
	for tag in panel.find_all(True, recursive=False):
		if not found and tag.get_text(strip=True) == "Nội Dung":
			found = True
			tag.decompose()
			break

	img_urls = []
	for img in panel.find_all("img"):
		img_url = img.get("data-src") or (
			img["data-srcset"].split(",")[0].strip() if img.has_attr("data-srcset") else None
		)
		if not img_url and img.has_attr("src") and img["src"].startswith("http"):
			img_url = img["src"]

		if img_url and img_url.startswith("http"):
			if item_code:
				frappe_img_url = download_and_attach_image(img_url, "Omni Item", item_code, None)
				img["src"] = frappe_img_url if frappe_img_url else img_url
			else:
				img["src"] = img_url  # Keep original URL
				img_urls.append(img_url)

	# Remove empty tags
	empty_tags = [
		tag
		for tag in panel.find_all()
		if tag.name not in ["br", "hr", "img", "style", "script"]
		and not tag.text.strip()
		and not tag.find("img")
	]
	for tag in empty_tags:
		tag.decompose()

	result = panel.decode_contents().strip()
	return result, img_urls

