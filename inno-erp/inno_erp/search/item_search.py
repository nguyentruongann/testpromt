import frappe
from erpnext import get_default_company
from erpnext.accounts.doctype.pos_invoice.pos_invoice import (
	get_stock_availability,
)
from frappe import _
from frappe.utils import flt, nowdate
from redis.commands.search.field import NumericField, TagField, TextField

from inno_erp.inno_omnichannel.doctype.omni_item.omni_item import (
	format_media_of_item,
	get_variant_attributes,
)

from .redis_search import RedisFullTextSearch

ITEM_FIELDS = [
	"name",
	"linked_item as item_code",
	"item_name",
	"image",
	"brand",
	"item_group",
	"short_description",
	"description",
	"has_variants",
	"video",
	"attach_image_1",
	"attach_image_2",
	"attach_image_3",
	"attach_image_4",
	"attach_image_5",
	"attach_360_image_1",
	"attach_360_image_2",
	"attach_360_image_3",
	"attach_360_image_4",
	"attach_360_image_5",
	"attach_360_image_6",
	"attach_360_image_7",
	"attach_360_image_8",
	"_user_tags",
	"creation",
]

NO_PROMO = "[]"

VARIANT_ITEM_FIELDS = [
	"name",
	"linked_item as item_code",
	"item_name",
	"image",
	# "short_description",
	# "description",
	"video",
	"attach_image_1",
	"attach_image_2",
	"attach_image_3",
	"attach_image_4",
	"attach_image_5",
	"attach_360_image_1",
	"attach_360_image_2",
	"attach_360_image_3",
	"attach_360_image_4",
	"attach_360_image_5",
	"attach_360_image_6",
	"attach_360_image_7",
	"attach_360_image_8",
	"_user_tags",
	"creation",
]

BATCH_SIZE = 500


class ItemSearch(RedisFullTextSearch):
	def __init__(self):
		super().__init__(ItemSearch.__name__)

	def get_schema(self):
		return (
			TextField("$.name", as_name="name"),
			TextField("$.item_name", as_name="item_name"),
			TextField("$.item_code", as_name="item_code"),
			TextField("$.description", as_name="description"),
			TextField("$.brand", as_name="brand"),
			TextField("$.item_group", as_name="item_group"),
			TagField("$.label", as_name="label"),
			NumericField("$.has_variants", as_name="has_variants"),
			NumericField("$.rate", as_name="rate"),
			NumericField("$.sold_quantity", as_name="sold_quantity"),
			NumericField("$.out_of_stock", as_name="out_of_stock"),
			NumericField("$.discount_amount", as_name="discount_amount"),
			NumericField("$.discount_percentage", as_name="discount_percentage"),
			NumericField("$.is_combo", as_name="is_combo"),
			NumericField("$.has_pricing_rules", as_name="has_pricing_rules"),
			NumericField("$.creation", as_name="creation"),
			TextField("$.pricing_rules", as_name="pricing_rules"),
			TextField("$.variants[*].attributes[*].attribute", as_name="attributes"),
			TextField(
				"$.variants[*].attributes[*].attribute_value",
				as_name="attribute_values",
			),
			TextField("$.specifications[*].specification", as_name="specifications"),
			TextField(
				"$.specifications[*].specification_value",
				as_name="specification_values",
			),
		)

	def get_items_to_index(self):
		filter_non_variant_items = {
			"disabled": 0,
			"variant_of": None,
		}

		total = frappe.db.count("Omni Item", filters=filter_non_variant_items)
		total_batches = total // BATCH_SIZE + 1

		selling_warehouses = [
			warehouse.custom_selling_warehouse
			for warehouse in frappe.db.get_all("Branch", fields=["custom_selling_warehouse"])
		]

		idx_items = []

		for batch_idx in range(total_batches):
			items = frappe.db.get_all(
				"Omni Item",
				filters=filter_non_variant_items,
				order_by="creation asc",
				fields=ITEM_FIELDS,
				limit_page_length=BATCH_SIZE,
				limit_start=batch_idx * BATCH_SIZE,
			)

			for item in items:
				load_item_with_full_data(item, selling_warehouses)
				idx_items.append(item)

		return idx_items

	def get_document_to_index(self, doc_name):
		item = frappe.db.get_value("Omni Item", doc_name, ITEM_FIELDS, as_dict=1)

		selling_warehouses = [
			warehouse.custom_selling_warehouse
			for warehouse in frappe.db.get_all("Branch", fields=["custom_selling_warehouse"])
		]

		load_item_with_full_data(item, selling_warehouses)
		return item

	def parse_result(self, result):
		item = frappe.parse_json(result)
		item.has_variants = item.has_variants or 0

		if item.has_variants:
			item.pop("price_list_rate")
			item.pop("discount_percentage")
			item.pop("discount_amount")
			item.pop("rate")
			item.pop("free_item_data")
			item.pop("pricing_rules")
			item.pop("price_or_product_discount")
			item.pop("pricing_rule_for")

		return item


def check_out_of_stock_by_numberic(item_code, warehouses):
	if not item_code:
		return 1

	for warehouse in warehouses:
		stock_availability, is_stock_item = get_stock_availability(item_code, warehouse)
		if not is_stock_item:
			return 0

		if stock_availability > 0:
			return 0

	return 1


def count_sold_quantity(item_codes):
	if not item_codes:
		return {}

	parent = frappe.qb.DocType("Sales Invoice")
	child = frappe.qb.DocType("Sales Invoice Item")

	query = (
		frappe.qb.from_(parent)
		.from_(child)
		.select(
			child.item_code,
			frappe.query_builder.functions.Sum(child.stock_qty).as_("sold_qty"),
		)
		.where((parent.docstatus == 1) & (parent.name == child.parent) & (child.item_code.isin(item_codes)))
		.groupby(child.item_code)
	)

	result = query.run(as_dict=True)
	sold_quantities = {row.item_code: flt(row.sold_qty) for row in result}
	return sold_quantities


def load_item_with_full_data(item, selling_warehouses):
	item = format_media_of_item(item)
	item.creation = int(item.creation.timestamp()) if item.creation else 0
	item.label = item.pop("_user_tags")
	if item.label and item.label.startswith(","):
		item.label = item.label[1:]

	item.specifications = frappe.get_all(
		"Item Specification",
		filters={"parent": item.name},
		fields=[
			"spec_name as specification",
			"spec_value as specification_value",
		],
	)

	if item.has_variants:
		load_variant_item(item, selling_warehouses)
		item.update(find_best_pricing_rule(item.variants))
		# check any variant has pricing rules
		item.has_pricing_rules = 0
		for variant in item.variants:
			if variant.pricing_rules != NO_PROMO:
				item.has_pricing_rules = 1
				break

	else:
		load_nonvariant_item(item, selling_warehouses)
		item.has_pricing_rules = 1 if item.pricing_rules != NO_PROMO else 0


def find_best_pricing_rule(variants):
	best_promo_variant = None
	best_discount_amount = 0

	for variant in variants:
		if not variant.discount_amount:
			continue

		if variant.discount_amount > best_discount_amount:
			best_discount_amount = variant.discount_amount
			best_promo_variant = variant

	if not best_promo_variant:
		return {
			"price_list_rate": 0,
			"discount_percentage": 0,
			"discount_amount": 0,
			"rate": 0,
			"free_item_data": [],
			"pricing_rules": NO_PROMO,
			"price_or_product_discount": "",
			"pricing_rule_for": "",
		}

	return {
		"price_list_rate": best_promo_variant.price_list_rate,
		"discount_percentage": best_promo_variant.discount_percentage,
		"discount_amount": best_promo_variant.discount_amount,
		"rate": best_promo_variant.rate,
		"free_item_data": best_promo_variant.free_item_data,
		"pricing_rules": best_promo_variant.pricing_rules,
		"price_or_product_discount": best_promo_variant.price_or_product_discount,
		"pricing_rule_for": best_promo_variant.pricing_rule_for,
	}


def load_variant_item(item, selling_warehouses):
	attributes = get_variant_attributes(item.name)

	item.variants = frappe.db.get_all(
		"Omni Item",
		filters={"variant_of": item.name},
		fields=VARIANT_ITEM_FIELDS,
	)

	sold_quantity_map = count_sold_quantity([variant.item_code for variant in item.variants])

	for variant in item.variants:
		variant = format_media_of_item(variant)
		variant.creation = int(variant.creation.timestamp()) if variant.creation else 0
		variant.attributes = attributes.get(variant.name, [])

		variant.out_of_stock = check_out_of_stock_by_numberic(variant.item_code, selling_warehouses)
		variant.sold_quantity = sold_quantity_map.get(variant.item_code, 0)
		variant.update(inno_get_pricing_rule_for_item(variant.item_code))


def load_nonvariant_item(item, selling_warehouses):
	sold_quantity_map = count_sold_quantity([item.item_code])
	item.sold_quantity = sold_quantity_map.get(item.item_code, 0)

	item.out_of_stock = check_out_of_stock_by_numberic(item.item_code, selling_warehouses)
	item.update(inno_get_pricing_rule_for_item(item.item_code))


from erpnext.accounts.doctype.pricing_rule.pricing_rule import get_pricing_rule_for_item
from erpnext.stock.get_item_details import (
	get_price_list_rate_for,
)

from inno_erp.inno_account.overrides.pricing_rule.pricing_rule import (
	get_all_pricing_rules_for_item,
)


def inno_get_pricing_rule_for_item(item_code):
	if not item_code:
		return {
			"price_list_rate": 0,
			"price_or_product_discount": "",
			"pricing_rule_for": "",
			"discount_percentage": 0,
			"discount_amount": 0,
			"rate": 0,
			"free_item_data": [],
			"pricing_rules": NO_PROMO,
		}

	DEFAULT_QTY = 1

	item_metadata = frappe.get_value("Omni Item", {"linked_item": item_code}, ["stock_uom"], as_dict=True)

	selling_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	price_list_rate = get_price_list_rate_for(
		{
			"customer": "Khách Lẻ",
			"transaction_date": nowdate(),
			"qty": DEFAULT_QTY,
			"uom": item_metadata.get("stock_uom"),
			"price_list": selling_price_list,
		},
		item_code,
	)

	price_list_rate = price_list_rate or 0.0
	if price_list_rate == 0:
		valuation_rate = frappe.db.get_value("Item", item_code, "valuation_rate") or 0
		if valuation_rate > 0:
			price_list_rate = valuation_rate
		else:
			frappe.msgprint(f"No price found for {item_code} in Price List 'Bán hàng' or Item master.")

	args = frappe._dict(
		{
			"items": [
				{
					"doctype": "Sales Order Item",
					"name": "preview_item",
					"item_code": item_code,
					"item_group": frappe.db.get_value("Item", item_code, "item_group"),
					"brand": frappe.db.get_value("Item", item_code, "brand"),
					"qty": DEFAULT_QTY,
					"stock_qty": DEFAULT_QTY,
					"price_list_rate": price_list_rate,
					"uom": item_metadata.get("stock_uom"),
					"stock_uom": item_metadata.get("stock_uom"),
					"parent": "preview",
					"parenttype": "Sales Order",
					"child_docname": "preview_item",
					"conversion_factor": 1,
					"discount_percentage": 0,
					"discount_amount": 0,
					"pricing_rules": "",
				}
			],
			"customer": "Khách Lẻ",
			"transaction_date": nowdate(),
			"company": get_default_company(),
			"transaction_type": "selling",
			"price_list": selling_price_list,
			"currency": frappe.get_value("Company", get_default_company(), "default_currency"),
			"conversion_rate": 1,
			"plc_conversion_rate": 1,
			"ignore_pricing_rule": 0,
		}
	)

	all_rules = get_all_pricing_rules_for_item(args)[0].get("pricing_rules_list", [])
	pricing_rules = [rule["pricing_rule"] for rule in all_rules]
	if len(pricing_rules) > 0:
		pricing_rules = pricing_rules[0]

	rule_args = frappe._dict(
		{
			"customer": "Khách Lẻ",
			"doctype": "Sales Order Item",
			"company": get_default_company(),
			"transaction_date": nowdate(),
			"transaction_type": "selling",
			"selling": 1,
			"buying": 0,
			"item_code": item_code,
			"qty": DEFAULT_QTY,
			"stock_qty": DEFAULT_QTY,
			"uom": item_metadata.get("stock_uom"),
			"price_list_rate": price_list_rate,
			"pricing_rules": frappe.as_json([pricing_rules]),
		}
	)
	rule = get_pricing_rule_for_item(args=rule_args, for_validate=True)

	calculated_rate = price_list_rate
	if rule.get("discount_amount", 0) > 0:
		calculated_rate = flt(calculated_rate) - flt(rule.get("discount_amount", 0))
	elif rule.get("discount_percentage", 0) > 0:
		calculated_rate = flt(calculated_rate) * (1 - flt(rule.get("discount_percentage", 0)) / 100)

	free_item_data = rule.get("free_item_data", [])
	for free_item in free_item_data:
		free_item["image"] = frappe.db.get_value("Omni Item", free_item.get("item_code"), "image")

	return {
		"price_list_rate": price_list_rate,
		"price_or_product_discount": rule.get("price_or_product_discount", ""),
		"pricing_rule_for": rule.get("pricing_rule_for", ""),
		"discount_percentage": rule.get("discount_percentage", 0),
		"discount_amount": rule.get("discount_amount", 0),
		"rate": calculated_rate if calculated_rate > 0 else 0,
		"free_item_data": free_item_data,
		"pricing_rules": rule.get("pricing_rules"),
	}


def build():
	item_search = ItemSearch()
	item_search.build()
