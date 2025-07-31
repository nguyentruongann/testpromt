import base64
import io
import json

import barcode
import frappe
from barcode.writer import ImageWriter
from erpnext.stock.doctype.item.item import Item
from frappe import _
from frappe.query_builder.functions import Count
from frappe.utils.nestedset import get_descendants_of

from inno_erp.utils.string import scrub


class InnoItem(Item):
	def autoname(self):
		if self.is_new() or self.has_value_changed("item_code"):
			self.item_code = scrub(self.item_code, separator="-")
		super().autoname()

	def validate(self):
		super().validate()

		if self.custom_is_combo:
			self.is_stock_item = 0

			combo_items = self.get("combo_items")
			if combo_items:
				if any(item.get("qty") <= 0 for item in combo_items):
					frappe.throw(_("Please ensure all items in the Combo have quantity greater than 0."))

				item_codes = [item.get("item_code") for item in combo_items]
				if len(item_codes) != len(set(item_codes)):
					frappe.throw(_("Combo can not have duplicate items."))

	def before_save(self):
		if len(self.barcodes) > 1:
			frappe.throw(_("An item can only have one barcode"))

		for b in self.barcodes:
			barcode_type = barcode.get_barcode_class("code128")
			options = {
				"font_size": 5,
				"module_height": 5,
				"text_distance": 2,
				"write_text": False,
			}
			barcode_instance = barcode_type(b.barcode, writer=ImageWriter())
			img_stream = io.BytesIO()
			barcode_instance.write(img_stream, options=options)
			img_base64 = base64.b64encode(img_stream.getvalue()).decode("utf-8")
			self.custom_barcode_data = f"data:image/png;base64,{img_base64}"

		if self.has_variants:
			variants = frappe.get_all(
				"Item", filters={"variant_of": self.name}, fields=["name", "valuation_rate"]
			)
			if len(variants) > 0:
				update_variant_prices(self.get("__variant_details"), self.get("__deleted_variant_details"))

		if self.custom_is_combo and not self.is_new():
			self.update_product_bundle()

	def after_insert(self):
		super().after_insert()
		if self.custom_is_combo:
			self.create_product_bundle()

	def create_product_bundle(self):
		combo_items = self._format_combo_items()
		if combo_items:
			if not frappe.db.exists("Product Bundle", self.name):
				product_bundle = frappe.new_doc("Product Bundle")
				product_bundle.new_item_code = self.name
				product_bundle.name = self.name
				product_bundle.set("items", combo_items)
				product_bundle.save(ignore_permissions=True)

	def update_product_bundle(self):
		combo_items = self._format_combo_items()
		if combo_items:
			product_bundle = frappe.get_doc("Product Bundle", self.name)
			current_items = [
				{
					"item_code": i.item_code,
					"qty": i.qty,
					"description": i.description,
					"uom": i.uom,
				}
				for i in product_bundle.items
			]
			if combo_items != current_items:
				product_bundle.set("items", combo_items)
				product_bundle.save(ignore_permissions=True)

	def on_update(self):
		if not self.has_variants:
			if self.standard_rate:
				upsert_item_price(
					self.name,
					frappe.db.get_single_value("Selling Settings", "selling_price_list"),
					self.stock_uom,
					self.standard_rate,
				)

	def on_trash(self):
		if self.custom_is_combo:
			bundle_name = self.name
			if frappe.db.exists("Product Bundle", bundle_name):
				frappe.delete_doc("Product Bundle", bundle_name, ignore_permissions=True)
		super().on_trash()

	def _format_combo_items(self):
		combo_items = self.get("combo_items")
		product_bundle_items = []
		if combo_items:
			if any(item.get("qty") <= 0 for item in combo_items):
				frappe.throw(_("Please ensure all items in the Combo have quantity greater than 0."))
			for item_dict in combo_items:
				product_bundle_items.append(
					{
						"item_code": item_dict.get("item_code"),
						"qty": item_dict.get("qty"),
						"description": item_dict.get("description"),
						"uom": item_dict.get("uom"),
					}
				)
		return product_bundle_items


# TODO(bao): Deprecated
@frappe.whitelist()
def setup_barcode(value, field, docname):
	frappe.db.set_value("Item", docname, {field: value})


@frappe.whitelist()
def get_items_by_item_groups(item_groups):
	items = []
	for item_group in json.loads(item_groups):
		children = [
			*get_descendants_of("Item Group", item_group["item_group"], ignore_permissions=True),
			item_group["item_group"],
		]
		items += frappe.get_all(
			"Item",
			filters={"item_group": ("in", children), "has_variants": ("!=", 1)},
			fields=["name", "item_name", "item_group"],
		)
	return list(map(dict, {tuple(d.items()) for d in items}))


# TODO: will be deleted
@frappe.whitelist()
def get_item_code(item_group="", brand=""):
	group_abbr = frappe.get_value("Item Group", item_group, "custom_abbr")
	brand_abbr = frappe.get_value("Brand", brand, "custom_abbr")
	return f"{group_abbr if group_abbr else ''}" + (f"-{brand_abbr}" if brand_abbr else "")


# TODO: should be used db.get_list
@frappe.whitelist()
def get_items_by_item_group_and_brand(doctype, txt, searchfield, start, page_len, filters=None):
	item_group = filters.get("item_group")
	brand = filters.get("brand")

	Item = frappe.qb.DocType("Item")

	query = (
		frappe.qb.from_(Item)
		.select(Item.name, Item.item_name, Item.item_group)
		.limit(page_len)
		.offset(start)
		.where(Item.has_variants == 0)
	)

	if txt:
		query = query.where((Item.name.like(f"%{txt}%")) | (Item.item_name.like(f"%{txt}%")))

	if item_group:
		query = query.where(Item.item_group == item_group)
	if brand:
		query = query.where(Item.brand == brand)

	results = query.run(as_dict=False)
	return results


# -----------------------------Update Price Dialog-----------------------------
@frappe.whitelist()
def get_detail_variants(template_item_code):
	try:
		template_data = frappe.db.get_value(
			"Item", template_item_code, ["item_name", "has_variants"], as_dict=True
		)

		if not template_data:
			frappe.throw(_("Template item {0} not found").format(template_item_code))

		if not template_data.has_variants:
			frappe.throw(_("Item {0} is not a template item").format(template_item_code))

		selling_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")

		Item = frappe.qb.DocType("Item")
		UOMConversion = frappe.qb.DocType("UOM Conversion Detail")
		ItemPrice = frappe.qb.DocType("Item Price")
		VariantAttribute = frappe.qb.DocType("Item Variant Attribute")

		query = (
			frappe.qb.from_(Item)
			.left_join(UOMConversion)
			.on(Item.name == UOMConversion.parent)
			.left_join(ItemPrice)
			.on(
				(Item.name == ItemPrice.item_code)
				& (UOMConversion.uom == ItemPrice.uom)
				& (ItemPrice.price_list == selling_price_list)
			)
			.left_join(VariantAttribute)
			.on(Item.name == VariantAttribute.parent)
			.select(
				Item.name.as_("variant_item_code"),
				UOMConversion.uom,
				(Item.valuation_rate * UOMConversion.conversion_factor).as_("valuation_rate"),
				ItemPrice.price_list_rate.as_("selling_rate"),
				(UOMConversion.uom == Item.stock_uom).as_("is_base_uom"),
				UOMConversion.conversion_factor,
				Item.valuation_rate.as_("base_valuation_rate"),
			)
			.where((Item.variant_of == template_item_code) & Item.disabled == 0)
			.orderby(Item.name)
			.orderby(UOMConversion.conversion_factor)
			.distinct()
		)

		results = query.run(as_dict=True)
		return {
			"status": "success",
			"rows": results,
		}

	except frappe.DoesNotExistError:
		frappe.throw(_("Template item {0} not found").format(template_item_code))
	except Exception as e:
		frappe.log_error(f"Error getting flattened variant details: {template_item_code}", str(e))
		frappe.throw(_("Error retrieving variant details: {0}").format(str(e)))
		return {"status": "error", "message": str(e)}


def upsert_item_price(item_code, price_list, uom, price_list_rate):
	existing_price = frappe.db.get_value(
		"Item Price",
		{"item_code": item_code, "price_list": price_list, "uom": uom},
		"name",
	)

	if not price_list:
		price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")

	if not existing_price:
		item_price = frappe.get_doc(
			{
				"doctype": "Item Price",
				"item_code": item_code,
				"price_list": price_list,
				"uom": uom,
				"price_list_rate": price_list_rate,
			}
		)
		item_price.insert(ignore_permissions=True)
	else:
		frappe.db.set_value("Item Price", existing_price, "price_list_rate", price_list_rate)


def update_variant_prices(variant_details, deleted_items=None):
	"""
	Update prices for variant items - only handles update existing and delete
	"""
	try:
		if isinstance(variant_details, str):
			variant_details = frappe.parse_json(variant_details)

		if isinstance(deleted_items, str):
			deleted_items = frappe.parse_json(deleted_items)

		deleted_items = deleted_items or []

		selling_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")

		if not selling_price_list:
			return {"status": "error", "message": "No selling price list configured"}

		errors = []

		# Handle UPDATE operations
		for variant in variant_details:
			try:
				variant_code = variant.get("variant_item_code")
				uom = variant.get("uom")
				valuation_rate = variant.get("valuation_rate", 0)
				selling_rate = variant.get("selling_rate", 0)

				if not variant_code or not uom:
					continue

				if variant.get("is_base_uom"):
					frappe.db.set_value("Item", variant_code, "valuation_rate", valuation_rate)

				if not (selling_rate > 0):
					continue

				upsert_item_price(variant_code, selling_price_list, uom, selling_rate)

			except Exception as e:
				errors.append(f"Error updating {variant_code}: {e!s}")

		# Handle DELETE operations
		for variant in deleted_items:
			try:
				variant_code = variant.get("variant_item_code")
				uom = variant.get("uom")

				existing_price = frappe.db.get_value(
					"Item Price",
					{"item_code": variant_code, "price_list": selling_price_list, "uom": uom},
					"name",
				)

				if existing_price:
					frappe.delete_doc("Item Price", existing_price, ignore_permissions=True)

			except Exception as e:
				errors.append(f"Error deleting price for {variant_code}: {e!s}")

		frappe.db.commit()

		result = {
			"status": "success",
		}

		if errors:
			result["status"] = "error"
			result["message"] = errors

		return result

	except Exception as e:
		frappe.log_error(f"Error updating variant prices: {e!s}")
		return {"status": "error", "message": str(e)}
