# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

# import frappe
import json

import frappe
from erpnext.controllers.item_variant import (
	copy_attributes_to_variant,
	generate_keyed_value_combinations,
	make_variant_item_code,
)
from erpnext.utilities.product import get_item_codes_by_attributes
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import strip
from frappe.utils.data import cstr

from inno_erp.utils.string import scrub


class OmniItem(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from erpnext.stock.doctype.item_variant_attribute.item_variant_attribute import ItemVariantAttribute
		from frappe.types import DF

		from inno_erp.inno_stock.doctype.item_specification.item_specification import ItemSpecification

		attach_360_image_1: DF.AttachImage | None
		attach_360_image_2: DF.AttachImage | None
		attach_360_image_3: DF.AttachImage | None
		attach_360_image_4: DF.AttachImage | None
		attach_360_image_5: DF.AttachImage | None
		attach_360_image_6: DF.AttachImage | None
		attach_360_image_7: DF.AttachImage | None
		attach_360_image_8: DF.AttachImage | None
		attach_image_1: DF.AttachImage | None
		attach_image_2: DF.AttachImage | None
		attach_image_3: DF.AttachImage | None
		attach_image_4: DF.AttachImage | None
		attach_image_5: DF.AttachImage | None
		attributes: DF.Table[ItemVariantAttribute]
		brand: DF.Link | None
		category: DF.Data | None
		description: DF.TextEditor | None
		disabled: DF.Check
		has_variants: DF.Check
		image: DF.AttachImage | None
		is_stock_item: DF.Check
		item_code: DF.Data
		item_group: DF.Link
		item_name: DF.Data | None
		item_specifications: DF.Table[ItemSpecification]
		linked_item: DF.Link | None
		naming_series: DF.Literal["OMN-ITEM-.YYYY.-"]
		platform: DF.Literal["Website", "Lazada", "Tiktok Shop", "Shopee"]
		shop: DF.Link | None
		short_description: DF.TextEditor | None
		specification_template: DF.Link | None
		stock_uom: DF.Link
		variant_based_on: DF.Literal["Item Attribute"]
		variant_of: DF.Link | None
		video: DF.Data | None
		waiting_orders: DF.Int
	# end: auto-generated types
	pass

	def autoname(self):
		if self.is_new() or self.has_value_changed("item_code"):
			self.item_code = scrub(self.item_code, separator="-")

		if frappe.db.get_default("item_naming_by") == "Naming Series":
			if self.variant_of:
				if not self.item_code:
					template_item_name = frappe.db.get_value("Omni Item", self.variant_of, "item_name")
					make_variant_item_code(self.variant_of, template_item_name, self)
			else:
				from frappe.model.naming import set_name_by_naming_series

				set_name_by_naming_series(self)
				self.item_code = self.name

		self.item_code = strip(self.item_code)
		self.name = self.item_code

	def validate(self):
		if self.linked_item:
			item_mapped = frappe.db.get_all(
				"Omni Item",
				filters={"linked_item": self.linked_item, "name": ("!=", self.name)},
			)
			if item_mapped:
				frappe.throw(
					_("The item {0} was linked to {1}").format(self.linked_item, item_mapped[0].name),
					title=_("Item was linked"),
				)

	def on_trash(self):
		for variant_of in frappe.get_all("Omni Item", filters={"variant_of": self.item_code}):
			frappe.delete_doc("Omni Item", variant_of.name)


def format_media_of_item(item: dict):
	media_fields = [
		"attach_image_1",
		"attach_image_2",
		"attach_image_3",
		"attach_image_4",
		"attach_image_5",
	]

	media_360_fields = [
		"attach_360_image_1",
		"attach_360_image_2",
		"attach_360_image_3",
		"attach_360_image_4",
		"attach_360_image_5",
		"attach_360_image_6",
		"attach_360_image_7",
		"attach_360_image_8",
	]
	item["image_urls"] = []
	item["image_360_urls"] = []

	for field in media_fields:
		if item.get(field):
			item["image_urls"].append(item[field])
		item.pop(field)

	for field in media_360_fields:
		if item.get(field):
			item["image_360_urls"].append(item[field])
		item.pop(field)

	return item


def get_variant_attributes(template_code):
	variants = frappe.db.get_list("Omni Item", filters={"variant_of": template_code})
	item_variant_attributes = {}
	for variant in variants:
		for t in frappe.get_all(
			"Item Variant Attribute",
			fields=["attribute", "attribute_value"],
			filters={"parent": variant.name},
		):
			item_variant_attributes.setdefault(variant.name, []).append(
				{
					"attribute": t.attribute,
					"attribute_value": t.attribute_value,
				}
			)
	return item_variant_attributes


@frappe.whitelist()
def make_omni_item(source_name, target_doc=None, ignore_permissions=False):
	def postprocess(source, target):
		set_missing_values(source, target)

	def set_missing_values(source, target):
		target.flags.ignore_permissions = True
		target.linked_item = None

		if not source.get("variant_of"):
			target.variant_of = None

		if not target.naming_series:
			target.naming_series = "OMN-ITEM-.YYYY.-"

		target.run_method("set_missing_values")
		target.run_method("validate")

	doclist = get_mapped_doc(
		"Item",
		source_name,
		{
			"Item": {
				"doctype": "Omni Item",
				"field_map": {
					"item_code": "item_code",
					"item_name": "item_name",
					"item_group": "item_group",
					"stock_uom": "stock_uom",
					"description": "description",
					"brand": "brand",
					"disabled": "disabled",
					"is_stock_item": "is_stock_item",
					"has_variants": "has_variants",
					"variant_based_on": "variant_based_on",
					"variant_of": "variant_of",
					"image": "image",
				},
				"validation": {"disabled": ["!=", 1]},
			},
			"Item Variant Attribute": {
				"doctype": "Item Variant Attribute",
				"field_map": {},
			},
			"Item Specification": {
				"doctype": "Item Specification",
				"field_map": {},
			},
		},
		target_doc,
		postprocess,
		ignore_permissions=ignore_permissions,
	)
	doclist.linked_item = source_name
	if doclist.has_variants:
		create_omni_item_variants(doclist.item_code)

	return doclist


def create_omni_item_variants(item_code):
	variants = frappe.get_all("Omni Item", filters={"variant_of": item_code})

	for variant in variants:
		create_omni_item_variant(variant.name)


def create_omni_item_variant(item_code):
	try:
		existing_omni_item = frappe.db.exists("Omni Item", {"linked_item": item_code})

		if existing_omni_item:
			frappe.msgprint(
				_("Omni Item already exists for {0}").format(item_code),
				title=_("Omni Item already exists"),
			)
			return existing_omni_item

		omni_item = make_omni_item(item_code, ignore_permissions=True)

		if omni_item:
			omni_item.save(ignore_permissions=True)
			return omni_item.name

	except Exception as e:
		frappe.throw(_("Failed to create Omni Item for variant {0}: {1}").format(item_code, str(e)))


@frappe.whitelist()
def get_omni_item_attribute(parent, attribute_value=""):
	"""Used for providing auto-completions in child table."""
	if not frappe.has_permission("Omni Item"):
		frappe.throw(_("No Permission"))

	results = frappe.get_all(
		"Item Attribute Value",
		fields=["attribute_value"],
		filters={"parent": parent, "attribute_value": ("like", f"%{attribute_value}%")},
		order_by="idx asc",
		limit=100,
	)

	return results


@frappe.whitelist()
def update_linked_item(doc_name, linked_item=None):
	doc = frappe.get_doc("Omni Item", doc_name)

	if doc.linked_item == linked_item:
		return

	doc.linked_item = linked_item or None
	doc.save(ignore_permissions=True)

	if linked_item:
		return _("The linked item for {0} has been updated to {1}.").format(doc_name, linked_item)
	else:
		return _("The linked item for {0} has been removed.").format(doc_name)


@frappe.whitelist()
def get_variant(template, args=None, variant=None, manufacturer=None, manufacturer_part_no=None):
	item_template = frappe.get_doc("Omni Item", template)

	if item_template.variant_based_on == "Manufacturer" and manufacturer:
		return make_variant_based_on_manufacturer(item_template, manufacturer, manufacturer_part_no)

	if isinstance(args, str):
		args = json.loads(args)

	attribute_args = {k: v for k, v in args.items() if k != "use_template_image"}
	if not attribute_args:
		frappe.throw(_("Please specify at least one attribute in the Attributes table"))

	return find_variant(template, args, variant)


def make_variant_based_on_manufacturer(template, manufacturer, manufacturer_part_no):
	"""Make and return a new variant based on manufacturer and
	manufacturer part no"""
	from frappe.model.naming import append_number_if_name_exists

	variant = frappe.new_doc("Omni Item")

	copy_attributes_to_variant(template, variant)

	variant_name = f"{template.name} - {manufacturer}"
	if manufacturer_part_no:
		variant_name += f" - {manufacturer_part_no}"

	variant.item_code = append_number_if_name_exists("Omni Item", variant_name)
	variant.flags.ignore_mandatory = True
	variant.save()

	if not frappe.db.exists("Item Manufacturer", {"item_code": variant.name, "manufacturer": manufacturer}):
		manufacturer_doc = frappe.new_doc("Item Manufacturer")
		manufacturer_doc.update(
			{
				"item_code": variant.name,
				"manufacturer": manufacturer,
				"manufacturer_part_no": manufacturer_part_no,
			}
		)

		manufacturer_doc.flags.ignore_mandatory = True
		manufacturer_doc.save(ignore_permissions=True)

	return variant


def find_variant(template, args, variant_item_code=None):
	possible_variants = [i for i in get_item_codes_by_attributes(args, template) if i != variant_item_code]

	for variant in possible_variants:
		variant = frappe.get_doc("Omni Item", variant)

		if len(args.keys()) == len(variant.get("attributes")):
			# has the same number of attributes and values
			# assuming no duplication as per the validation in Item
			match_count = 0

			for attribute, value in args.items():
				for row in variant.attributes:
					if row.attribute == attribute and row.attribute_value == cstr(value):
						# this row matches
						match_count += 1
						break

			if match_count == len(args.keys()):
				return variant.name


@frappe.whitelist()
def create_variant(item, args, use_template_image=False):
	use_template_image = frappe.parse_json(use_template_image)
	if isinstance(args, str):
		args = json.loads(args)

	template = frappe.get_doc("Omni Item", item)
	variant = frappe.new_doc("Omni Item")
	variant.variant_based_on = "Item Attribute"
	variant_attributes = []

	for d in template.attributes:
		variant_attributes.append({"attribute": d.attribute, "attribute_value": args.get(d.attribute)})

	variant.set("attributes", variant_attributes)
	copy_attributes_to_variant(template, variant)

	if use_template_image and template.image:
		variant.image = template.image

	make_variant_item_code(template.item_code, template.item_name, variant)

	return variant


@frappe.whitelist()
def enqueue_multiple_variant_creation(item, args, use_template_image=False):
	use_template_image = frappe.parse_json(use_template_image)
	# There can be innumerable attribute combinations, enqueue
	if isinstance(args, str):
		variants = json.loads(args)
	total_variants = 1
	for key in variants:
		total_variants *= len(variants[key])
	if total_variants >= 600:
		frappe.throw(_("Please do not create more than 500 items at a time"))
		return
	if total_variants < 10:
		return create_multiple_variants(item, args, use_template_image)
	else:
		frappe.enqueue(
			"inno_erp.inno_omnichannel.doctype.omni_item.omni_item.create_multiple_variants",
			item=item,
			args=args,
			use_template_image=use_template_image,
			now=frappe.flags.in_test,
		)
		return "queued"


def create_multiple_variants(item, args, use_template_image=False):
	count = 0
	if isinstance(args, str):
		args = json.loads(args)

	template_item = frappe.get_doc("Omni Item", item)
	args_set = generate_keyed_value_combinations(args)
	for attribute_values in args_set:
		if not get_variant(item, args=attribute_values):
			variant = create_variant(item, attribute_values)
			if use_template_image and template_item.image:
				variant.image = template_item.image
			variant.save()
			count += 1

	return count
