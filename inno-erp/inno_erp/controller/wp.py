import frappe
from erpnext import get_default_company
from erpnext.accounts.doctype.pos_invoice.pos_invoice import (
	get_stock_availability as get_stock_availability_erpnext,
)
from frappe import _
from frappe.utils import cint, nowdate
from pydantic import BaseModel
from redis.commands.search.query import Query

from inno_erp.search.item_search import ItemSearch

ORDER_BY_MAP = {
	"CREATION_DESC": ("creation", False),
	"CREATION_ASC": ("creation", True),
	"PRICE_ASC": ("rate", True),
	"PRICE_DESC": ("rate", False),
	"BEST_SELLING": ("sold_quantity", False),
	"BEST_DISCOUNT_AMOUNT": ("discount_amount", False),
	"BEST_DISCOUNT_PERCENT": ("discount_percentage", False),
}


@frappe.whitelist()
def search_items(query="*", limit=5, limit_start=0, order_by="CREATION_DESC"):
	limit = cint(limit)
	order_by_field, order_by_asc = ORDER_BY_MAP.get(order_by, ("creation", False))

	item_search = ItemSearch()
	results_json, total_count = item_search.search(
		Query(f"*{ItemSearch.escape_query(query)}*")
		.sort_by(order_by_field, asc=order_by_asc)
		.paging(limit_start, limit)
	)

	return {"data": results_json, "total_count": total_count}


@frappe.whitelist(methods=["GET"])
def detail_item(item_code: str):
	item_search = ItemSearch()
	results_json, total_count = item_search.search(
		Query(f"@item_code:{ItemSearch.escape_query(item_code)}").paging(0, 1)
	)
	if not results_json:
		frappe.throw(_("Item not found"))

	return results_json[0]


@frappe.whitelist(methods=["GET"])
def list_variant(item_groups: str | None = None):
	attributes = []

	if not item_groups:
		attributes = frappe.db.sql(
			"""
				SELECT iva.attribute, i.item_group, i.brand from `tabItem Variant Attribute` iva
				LEFT JOIN `tabOmni Item` i on iva.parent = i.name
				GROUP BY iva.attribute, i.item_group, i.brand
			""",
			as_dict=True,
		)
	else:
		attributes = frappe.db.sql(
			"""
				SELECT iva.attribute, i.item_group, i.brand from `tabItem Variant Attribute` iva
				LEFT JOIN `tabOmni Item` i on iva.parent = i.name
				WHERE i.item_group IN %(item_groups)s
				GROUP BY iva.attribute, i.item_group, i.brand
			""",
			{"item_groups": frappe.parse_json(item_groups)},
			as_dict=True,
		)

	attribute_values = frappe.db.get_all(
		"Item Attribute Value",
		filters={"parent": ["in", [attr.attribute for attr in attributes]]},
		fields=["parent", "attribute_value"],
		order_by="attribute_value asc",
	)

	attribute_result = {}
	for attr in attributes:
		attribute_name = attr.attribute
		attribute_result[attribute_name] = [
			attr_value.attribute_value
			for attr_value in attribute_values
			if attr_value.parent == attribute_name
		]

	return attribute_result


@frappe.whitelist(methods=["GET"])
def list_all_item_groups():
	root_item_group = frappe.db.get_value("Item Group", {"lft": 1})
	item_groups = frappe.db.get_all(
		"Item Group",
		filters={"parent_item_group": root_item_group},
		fields=["name", "lft", "rgt"],
		order_by="lft asc",
	)

	for group in item_groups:
		group["children"] = []

	level_2_item_groups = frappe.db.get_all(
		"Item Group",
		filters={"parent_item_group": ["!=", root_item_group]},
		fields=["name", "lft", "rgt"],
		order_by="lft asc",
	)
	for child_group in level_2_item_groups:
		for parent_group in item_groups:
			if child_group.lft > parent_group.lft and child_group.rgt < parent_group.rgt:
				parent_group["children"].append(child_group)

	return item_groups


REDIS_SEPARATOR = " | "


def join_query_data(values: list[str]) -> str:
	return ItemSearch.escape_query(REDIS_SEPARATOR.join(values))


@frappe.whitelist(methods=["GET"])
def browse_items(
	brands: str | None = None,
	item_groups: str | None = None,
	labels: str | None = None,
	order_by: str | None = None,
	limit_start: int = 0,
	limit_page_length: int = 20,
	**kwargs,
):
	kwargs.pop("cmd")
	queries = []
	if brands and (brands := frappe.parse_json(brands)):
		queries.append(f"@brand:('{join_query_data(brands)}')")
	if item_groups and (item_groups := frappe.parse_json(item_groups)):
		queries.append(f"@item_group:('{join_query_data(item_groups)}')")
	if labels and (labels := frappe.parse_json(labels)):
		queries.append(f"@label:{{'{join_query_data(labels)}'}}")

	attibute_keys = []
	attibute_values = []

	for key, value in kwargs.items():
		attibute_keys.append(key)
		attibute_values = attibute_values + frappe.parse_json(value)

	if attibute_keys:
		queries.append(f"@attributes:('{join_query_data(attibute_keys)}')")
	if attibute_values:
		queries.append(f"@attribute_values:('{join_query_data(attibute_values)}')")

	order_by_field, order_by_asc = ORDER_BY_MAP.get(order_by, ("creation", False))

	query = " ".join(queries) if queries else "*"

	results_json, total_count = ItemSearch().search(
		Query(query).sort_by(order_by_field, asc=order_by_asc).paging(limit_start, limit_page_length)
	)
	return {"data": results_json, "total_count": total_count}


@frappe.whitelist(methods=["GET"])
def browse_promo_items(
	brands: str | None = None,
	item_groups: str | None = None,
	labels: str | None = None,
	order_by: str | None = None,
	limit_start: int = 0,
	limit_page_length: int = 20,
	**kwargs,
):
	kwargs.pop("cmd")
	queries = ["@has_pricing_rules:[(0 inf]"]
	if brands and (brands := frappe.parse_json(brands)):
		queries.append(f"@brand:('{join_query_data(brands)}')")
	if item_groups and (item_groups := frappe.parse_json(item_groups)):
		queries.append(f"@item_group:('{join_query_data(item_groups)}')")
	if labels and (labels := frappe.parse_json(labels)):
		queries.append(f"@label:{{'{join_query_data(labels)}'}}")

	attibute_keys = []
	attibute_values = []

	for key, value in kwargs.items():
		attibute_keys.append(key)
		attibute_values = attibute_values + frappe.parse_json(value)

	if attibute_keys:
		queries.append(f"@attributes:('{join_query_data(attibute_keys)}')")
	if attibute_values:
		queries.append(f"@attribute_values:('{join_query_data(attibute_values)}')")

	order_by_field, order_by_asc = ORDER_BY_MAP.get(order_by, ("creation", False))

	query = " ".join(queries) if queries else "*"

	results_json, total_count = ItemSearch().search(
		Query(query).sort_by(order_by_field, asc=order_by_asc).paging(limit_start, limit_page_length)
	)
	return {"data": results_json, "total_count": total_count}


@frappe.whitelist(methods=["GET"])
def get_stock_availability(item_codes: str, warehouses: str | None = None):
	item_codes = frappe.parse_json(item_codes)
	warehouses = frappe.parse_json(warehouses)
	if not warehouses:
		warehouses = frappe.db.get_all(
			"Branch",
			fields=["custom_selling_warehouse"],
			# How about multiple companies?
			# filters={"custom_company": get_default_company()
		)
		warehouses = [
			warehouse.custom_selling_warehouse
			for warehouse in warehouses
			if warehouse.custom_selling_warehouse
		]

	stock_availability = {}
	for item_code in item_codes:
		for warehouse in warehouses:
			if item_code not in stock_availability:
				stock_availability[item_code] = {}
			stock_availability[item_code][warehouse] = get_stock_availability_erpnext(item_code, warehouse)

	return stock_availability


class NewOrderItem(BaseModel):
	item_code: str
	qty: float


class NewOrder(BaseModel):
	customer: str
	transaction_date: str
	items: list[NewOrderItem]
	delivery_date: str | None = None
	company: str | None = None
	currency: str | None = None
	conversion_rate: float | None = None
	selling_price_list: str | None = None
	price_list_currency: str | None = None
	status: str | None = None
	phone: str | None = None
	address_title: str | None = None
	address_line1: str | None = None
	custom_address_location: str | None = None
	custom_ward: str | None = None
	custom_customers_request: str | None = None
	custom_pickup_at: str | None = None
	payment_mode: str | None = None
	delivery_vendor: str | None = None
	delivery_fee: float | None = None
	coupon_code: str | None = None


@frappe.whitelist(methods=["POST"])
def save_order(**kwargs):
	from inno_erp.search.item_search import NO_PROMO, inno_get_pricing_rule_for_item

	order = NewOrder.model_validate(kwargs)
	order_doc = frappe.new_doc("Sales Order")
	order_doc.customer = order.customer
	order_doc.order_type = "Sales" if kwargs.get("docstatus", 1) == 1 else "Shopping Cart"

	order_doc.company = order.company or get_default_company()
	order_doc.transaction_date = order.transaction_date
	order_doc.delivery_date = order.delivery_date or nowdate()

	order_doc.conversion_rate = order.conversion_rate or 1
	order_doc.currency = order.currency or frappe.get_value("Company", order.company, "currency")
	order_doc.selling_price_list = order.selling_price_list or frappe.get_value(
		"Selling Settings", None, "selling_price_list"
	)
	order_doc.price_list_currency = order.price_list_currency or frappe.get_value(
		"Price List", order_doc.selling_price_list, "currency"
	)
	order_doc.coupon_code = order.coupon_code

	if order.custom_customers_request:
		order_doc.custom_customers_request = order.custom_customers_request
	if order.custom_pickup_at and frappe.db.exists("Branch", order.custom_pickup_at):
		order_doc.set_warehouse = frappe.db.get_value(
			"Branch", order.custom_pickup_at, "custom_selling_warehouse"
		)

	coupon_rule = None
	if order_doc.coupon_code:
		coupon_rule = frappe.db.get_value("Coupon Code", order_doc.coupon_code, "pricing_rule")

	for item in order.items:
		rule = inno_get_pricing_rule_for_item(item.item_code)
		rules = []

		if rule.get("pricing_rules") != NO_PROMO:
			rules = frappe.parse_json(rule.get("pricing_rules"))

		if coupon_rule:
			rules.append(coupon_rule)
		omni_item = frappe.get_value("Omni Item", {"linked_item": item.item_code}, "item_name")
		order_doc.append(
			"items",
			{
				"item_code": item.item_code,
				"item_name": omni_item,
				"qty": item.qty,
				"pricing_rules": frappe.as_json(rules),
			},
		)

	order_doc.save()

	address = frappe.get_doc(
		{
			"doctype": "Address",
			"address_title": order.address_title,
			"address_line1": order.address_line1,
			"address_type": "Shipping",
			"city": order.custom_address_location,
			"custom_ward": order.custom_ward,
			"custom_address_location": order.custom_address_location,
			"country": "Vietnam",
			"is_primary_address": 0,
			"is_shipping_address": 1,
			"links": [{"link_doctype": "Customer", "link_name": order.customer}],
		}
	)
	address.insert()

	order_doc.shipping_address_name = address.name

	if order.delivery_vendor and order.delivery_fee:
		# TODO: Handle delivery fee for other vendors

		order_doc.append(
			"taxes",
			{
				"doctype": "Sales Taxes and Charges",
				"charge_type": "Actual",
				"description": f"Phí vận chuyển - {order.delivery_vendor}",
				# TODO: change right account
				"account_head": frappe.db.get_value("Company", get_default_company(), "default_bank_account"),
				"cost_center": frappe.db.get_value("Company", get_default_company(), "cost_center"),
				"tax_amount": order.delivery_fee,
			},
		)

	order_doc.save()

	if kwargs.get("docstatus", 1) != 0:
		order_doc.submit()
	frappe.db.commit()
	return order_doc


@frappe.whitelist(methods=["PUT"])
def cancel_order(order_name: str):
	order = frappe.get_doc("Sales Order", order_name)
	if order.status == "Cancelled":
		frappe.throw(_("Order already cancelled"))

	order.cancel()
	return "OK"


# TODO: TEMP CODEEEEEEEEEEEEEEEEE


class CalculateDeliveryFee(BaseModel):
	address_line1: str
	custom_ward: str
	custom_address_location: str


from inno_erp.libs.ghtk_api import GhtkApi
from inno_erp.libs.ghtk_api.typing import FeeRequest


@frappe.whitelist(methods=["POST"])
def calculate_delivery_fee(**kwargs):
	calculate_delivery_fee = CalculateDeliveryFee.model_validate(kwargs)
	province, district = calculate_delivery_fee.custom_address_location.split(" - ")
	ward = calculate_delivery_fee.custom_ward.split("-")[0]

	ghtk_api = GhtkApi(partner_code="S22927151", access_token="8MsWkQoYSAbrlsW8VXrXmc2rf2fAluZCHunOgQ")
	pick_address_id = ghtk_api.address.getListPickAdd().data[0].pick_address_id

	fee_result = ghtk_api.order.calculate_fee(
		FeeRequest(
			pick_address_id=pick_address_id,
			pick_province="Hồ Chí Minh",
			pick_district="Quận Bình Thạnh",
			address=calculate_delivery_fee.address_line1,
			province=province,
			district=district,
			ward=ward,
			weight=600,
			deliver_option="xteam",
		)
	)

	return {"GHTK": fee_result.fee.fee}


# TODO: END TEMP CODEEEEEEEEEEEEEEEEE


class UpdateCustomer(BaseModel):
	customer_id: str
	customer_name: str
	gender: str
	mobile_no: str
	email_id: str
	address_line1: str
	custom_ward: str
	custom_address_location: str


@frappe.whitelist(methods=["PUT"])
def update_customer(**kwargs):
	from frappe.contacts.doctype.address.address import get_address_display

	customer = UpdateCustomer.model_validate(kwargs)
	customer_primary_address = frappe.get_value("Customer", customer.customer_id, "customer_primary_address")
	customer_primary_contact = frappe.get_value("Customer", customer.customer_id, "customer_primary_contact")

	if not customer_primary_address:
		from inno_erp.inno_selling.overrides.customer.customer import inno_make_address

		address = inno_make_address(
			frappe._dict(
				doctype="Customer",
				name=customer.customer_id,
				address_line1=customer.address_line1,
				address_type="Shipping",
				custom_ward=customer.custom_ward,
				custom_address_location=customer.custom_address_location,
			)
		)
	else:
		address = frappe.get_doc("Address", customer_primary_address)
		address.address_line1 = customer.address_line1
		address.custom_ward = customer.custom_ward
		address.custom_address_location = customer.custom_address_location
		address.save()

	if not customer_primary_contact:
		from erpnext.selling.doctype.customer.customer import make_contact

		contact = make_contact(
			frappe._dict(
				doctype="Customer",
				name=customer.customer_id,
				customer_name=customer.customer_name,
				mobile_no=customer.mobile_no,
				email_id=customer.email_id,
			)
		)
	else:
		contact = frappe.get_doc("Contact", customer_primary_contact)
		contact.mobile_no = customer.mobile_no
		contact.email_id = customer.email_id
		contact.save()

	customer_doc = frappe.get_doc("Customer", customer.customer_id)
	customer_doc.customer_name = customer.customer_name
	customer_doc.gender = customer.gender
	customer_doc.mobile_no = customer.mobile_no
	customer_doc.email_id = customer.email_id
	customer_doc.customer_primary_contact = contact.name
	customer_doc.customer_primary_address = address.name
	customer_doc.primary_address = get_address_display(address.name)

	customer_doc.save()
	frappe.db.commit()
	return "OK"
