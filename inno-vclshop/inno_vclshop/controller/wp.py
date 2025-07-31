import frappe
from erpnext import get_default_company
from erpnext.accounts.doctype.pricing_rule.pricing_rule import get_pricing_rule_for_item
from erpnext.controllers.taxes_and_totals import calculate_taxes_and_totals
from erpnext.stock.dashboard.item_dashboard import get_data
from erpnext.stock.get_item_details import (
	get_conversion_factor,
	get_price_list_rate_for,
)
from frappe.utils import flt, nowdate
from inno_erp.inno_account.overrides.pricing_rule.pricing_rule import (
	get_all_pricing_rules_for_item,
	get_all_pricing_rules_for_transaction,
	inno_apply_transaction_pricing_rule,
)
from pydantic import BaseModel, ValidationError


class NewOrderItem(BaseModel):
	item_code: str
	qty: float
	pricing_rule: str


class NewOrder(BaseModel):
	customer: str
	pricing_rule: str
	items: list[NewOrderItem]
	phone: str | None = None
	address_title: str | None = None
	address_line1: str | None = None
	address_location: str | None = None
	ward: str | None = None
	customers_request: str | None = None
	payment_mode: str | None = None
	delivery_vendor: str | None = None
	delivery_fee: float | None = None
	coupon_code: str | None = None


class SalesOrderItemResp(BaseModel):
	item_code: str
	item_name: str
	price_list_rate: float
	qty: int
	rate: float
	discount_amount: float
	discount_percentage: float
	distributed_discount_amount: float
	amount: float
	is_free_item: bool
	image: str


class SalesOrderResp(BaseModel):
	name: str
	customer: str
	transaction_date: str
	status: str
	coupon_code: str | None = None
	total_taxes_and_charges: float
	grand_total: float
	discount_amount: float = 0.0
	additional_discount_percentage: float = 0.0
	coupon_discount_amount: float = 0.0
	coupon_discount_percentage: float = 0.0
	items: list[SalesOrderItemResp] = []


class Get_Pricing_Rule_Item(BaseModel):
	item_code: str
	qty: float


class Get_Pricing_Rule(BaseModel):
	total: float | None = None
	total_qty: float | None = None
	items: list[Get_Pricing_Rule_Item] = []


@frappe.whitelist(methods=["POST"])
def get_pricing_rule(**kwargs):
	try:
		validated_data = Get_Pricing_Rule(**kwargs)
	except ValidationError as e:
		frappe.throw(f"Invalid input data: {e!s}")

	items = validated_data.items
	input_total = validated_data.total
	input_total_qty = validated_data.total_qty

	if not items:
		frappe.throw("Items list cannot be empty.")

	company = get_default_company()
	if not company:
		frappe.throw("No default company found in the system.")

	price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	if not price_list:
		frappe.throw("No selling price list configured in Selling Settings.")

	item_rules = {}
	order_rules_dict = {}
	calculated_total_qty = 0.0
	calculated_total = 0.0
	price_list_rates = {}

	for item in items:
		item_code = item.item_code
		qty = flt(item.qty)

		if not item_code or qty <= 0:
			frappe.throw(f"Item code and valid quantity are required for item: {item_code}")

		calculated_total_qty += qty

		item_data = frappe.db.get_value("Item", item_code, ["item_group", "brand"], as_dict=True)
		if not item_data:
			frappe.throw(f"Item {item_code} not found in Item master.")

		item_metadata = frappe.get_value(
			"Omni Item", {"linked_item": item_code}, ["stock_uom"], as_dict=True
		) or frappe.get_value("Item", item_code, ["stock_uom"], as_dict=True)

		if not item_metadata or not item_metadata.get("stock_uom"):
			frappe.throw(f"Stock UOM not found for item {item_code}.")

		price_list_rate = (
			get_price_list_rate_for(
				{
					"customer": "Khách Lẻ",
					"transaction_date": nowdate(),
					"qty": qty,
					"uom": item_metadata.get("stock_uom"),
					"price_list": price_list,
				},
				item_code,
			)
			or 0.0
		)

		if price_list_rate == 0:
			valuation_rate = frappe.db.get_value("Item", item_code, "valuation_rate") or 0
			if valuation_rate > 0:
				price_list_rate = valuation_rate
			else:
				frappe.msgprint(
					f"No price found for {item_code} in Price List '{price_list}' or Item master."
				)

		price_list_rates[item_code] = price_list_rate
		calculated_total += flt(price_list_rate) * qty

		args = frappe._dict(
			{
				"items": [
					{
						"doctype": "Sales Order Item",
						"name": f"preview_{item_code}",
						"item_code": item_code,
						"item_group": item_data.get("item_group"),
						"brand": item_data.get("brand"),
						"qty": qty,
						"stock_qty": qty,
						"price_list_rate": price_list_rate,
						"uom": item_metadata.get("stock_uom"),
						"stock_uom": item_metadata.get("stock_uom"),
						"parent": "preview",
						"parenttype": "Sales Order",
						"child_docname": f"preview_{item_code}",
						"conversion_factor": 1,
						"discount_percentage": 0,
						"discount_amount": 0,
						"pricing_rules": "",
					}
				],
				"customer": "Khách Lẻ",
				"transaction_date": nowdate(),
				"company": company,
				"transaction_type": "selling",
				"price_list": price_list,
				"currency": frappe.get_value("Company", company, "default_currency"),
				"conversion_rate": 1,
				"plc_conversion_rate": 1,
				"ignore_pricing_rule": 0,
			}
		)

		pricing_rules_data = get_all_pricing_rules_for_item(args)
		if not pricing_rules_data or not isinstance(pricing_rules_data, list):
			frappe.msgprint(f"No pricing rules found for item {item_code}.")
			item_rules[item_code] = []
			continue

		item_rules_dict = {}
		for rule_data in pricing_rules_data:
			pricing_rules_list = rule_data.get("pricing_rules_list", [])
			for rule in pricing_rules_list:
				details = rule.get("details", {})
				promotion = details.get("promotional_scheme", "") or rule.get("title", "")
				description = details.get("rule_description", "") or ""

				if promotion not in item_rules_dict:
					item_rules_dict[promotion] = {"promotion": promotion, "rules": []}
				item_rules_dict[promotion]["rules"].append(
					{
						"pricing_rule": rule.get("pricing_rule"),
						"description": description,
					}
				)

		item_rules[item_code] = list(item_rules_dict.values())

	transaction_args = frappe._dict(
		{
			"transaction_type": "selling",
			"transaction_date": nowdate(),
			"company": company,
			"total_qty": input_total_qty if input_total_qty is not None else calculated_total_qty,
			"total": input_total if input_total is not None else calculated_total,
			"doctype": "Sales Order",
		}
	)

	transaction_rules_data = get_all_pricing_rules_for_transaction(transaction_args)
	order_rules = []
	if not transaction_rules_data:
		frappe.msgprint("No transaction pricing rules found.")
	else:
		pricing_rules_list = transaction_rules_data.get("pricing_rules_list", [])
		for rule in pricing_rules_list:
			details = rule.get("details", {})
			promotion = details.get("promotional_scheme", "") or rule.get("title", "")
			description = details.get("rule_description", "") or ""

			if promotion not in order_rules_dict:
				order_rules_dict[promotion] = {"promotion": promotion, "rules": []}
			order_rules_dict[promotion]["rules"].append(
				{"pricing_rule": rule.get("pricing_rule"), "description": description}
			)

		order_rules = list(order_rules_dict.values())

	return {"order_rules": order_rules, "item_rules": item_rules}


@frappe.whitelist(methods=["POST"])
def find_sufficient_warehouse(items):
	if not items:
		frappe.throw("Items list cannot be empty.")

	item_stock = {}
	all_warehouses = set()
	for item in items:
		item_code = item.item_code
		qty = item.qty
		if not item_code or qty <= 0:
			frappe.throw(f"Invalid item: {item}")

		stock_data = get_data(item_code=item_code)
		if not stock_data:
			return None

		item_stock[item_code] = {}
		for entry in stock_data:
			warehouse = entry.get("warehouse")
			actual_qty = entry.get("actual_qty", 0)
			item_stock[item_code][warehouse] = actual_qty
			all_warehouses.add(warehouse)

	sufficient_warehouses = []
	for warehouse in all_warehouses:
		sufficient = True
		for item in items:
			item_code = item.item_code
			qty = item.qty
			if warehouse not in item_stock[item_code] or item_stock[item_code][warehouse] < qty:
				sufficient = False
				break
		if sufficient:
			sufficient_warehouses.append(warehouse)

	return sufficient_warehouses[0] if sufficient_warehouses else None


@frappe.whitelist(methods=["POST"])
def make_sales_order(**kwargs):
	company = get_default_company()
	default_price_list = frappe.get_single_value("Selling Settings", "selling_price_list")

	order = NewOrder.model_validate(kwargs)
	order_doc = frappe.get_doc(
		{
			"doctype": "Sales Order",
			"customer": order.customer,
			"company": company,
			"transaction_date": nowdate(),
			"delivery_date": nowdate(),
			"conversion_rate": 1,
			"currency": frappe.get_value("Company", company, "default_currency"),
			"selling_price_list": default_price_list,
			"price_list_currency": frappe.get_value("Price List", default_price_list, "currency"),
		}
	)

	warehouse = find_sufficient_warehouse(order.items)
	if not warehouse:
		frappe.throw("No warehouse found with sufficient stock for all items")
	branch_name = frappe.db.get_value("Branch", {"custom_selling_warehouse": warehouse}, "name")
	if not branch_name:
		frappe.throw("Branch not found")
	branch = frappe.get_doc("Branch", branch_name)
	order_doc.set_warehouse = branch.custom_selling_warehouse

	if order.coupon_code:
		order_doc.coupon_code = order.coupon_code

	for item in order.items:
		rule = inno_get_pricing_rule_for_item(item, order.coupon_code)
		rules = []
		if rule.get("pricing_rules") != "[]":
			rules = frappe.parse_json(rule.get("pricing_rules"))

		omni_item = (
			frappe.get_value("Omni Item", {"linked_item": item.item_code}, "item_name") or item.item_code
		)
		order_doc.append(
			"items",
			{
				"item_code": item.item_code,
				"item_name": omni_item,
				"qty": item.qty,
				"pricing_rules": frappe.as_json(rules),
				"warehouse": branch.custom_selling_warehouse,
				"cost_center": branch.custom_cost_center,
				"price_list_rate": rule.get("price_list_rate", 0),
				"rate": rule.get("rate", 0),
				"base_price_list_rate": rule.get("price_list_rate", 0),
				"base_rate": rule.get("rate", 0),
				"amount": item.qty * rule.get("rate", 0),
				"base_amount": item.qty * rule.get("rate", 0),
				"net_rate": rule.get("rate", 0),
				"base_net_rate": rule.get("rate", 0),
				"net_amount": item.qty * rule.get("rate", 0),
				"base_net_amount": rule.get("rate", 0),
			},
		)

	address = frappe.get_doc(
		{
			"doctype": "Address",
			"address_title": order.address_title,
			"address_line1": order.address_line1,
			"address_type": "Shipping",
			"city": order.address_location,
			"custom_ward": order.ward,
			"custom_address_location": order.address_location,
			"country": "Vietnam",
			"is_primary_address": 0,
			"is_shipping_address": 1,
			"links": [{"link_doctype": "Customer", "link_name": order.customer}],
		}
	)
	address.insert()
	order_doc.shipping_address_name = address.name

	if order.customers_request:
		order_doc.custom_order_note = order.customers_request

	order_doc.save()
	order_doc.calculate_taxes_and_totals()
	rule_result = inno_apply_custom_pricing_rule_on_transaction(order_doc, order.pricing_rule)

	if order.delivery_vendor and order.delivery_fee:
		order_doc.append(
			"taxes",
			{
				"doctype": "Sales Taxes and Charges",
				"charge_type": "Actual",
				"description": f"Phí vận chuyển - {order.delivery_vendor}",
				"account_head": frappe.db.get_value("Company", get_default_company(), "default_bank_account"),
				"cost_center": frappe.db.get_value("Company", get_default_company(), "cost_center"),
				"tax_amount": order.delivery_fee,
			},
		)

	order_doc.save()

	if "docstatus" not in kwargs:
		frappe.db.rollback()
		order_dict = order_doc.as_dict()
		order_dict["coupon_discount_amount"] = rule_result.get("coupon_pricing_rule_discount_amount", 0.0)
		order_dict["coupon_discount_percentage"] = rule_result.get(
			"coupon_pricing_rule_discount_percentage", 0.0
		)
		return SalesOrderResp(**order_dict).model_dump()

	if kwargs.get("docstatus") == 1:
		order_doc = order_doc.submit()

	order_dict = order_doc.as_dict()
	order_dict["coupon_discount_amount"] = rule_result.get("coupon_pricing_rule_discount_amount", 0.0)
	order_dict["coupon_discount_percentage"] = rule_result.get("coupon_pricing_rule_discount_percentage", 0.0)
	return SalesOrderResp(**order_dict).model_dump()


def inno_apply_custom_pricing_rule_on_transaction(doc, transaction_pricing_rule=None):
	args = frappe._dict(
		{
			"transaction_type": "selling",
			"transaction_date": doc.transaction_date,
			"company": doc.company,
			"customer": doc.customer,
			"total_qty": doc.total_qty,
			"total": doc.total,
			"doctype": doc.doctype,
		}
	)

	all_rules = get_all_pricing_rules_for_transaction(args).get("pricing_rules_list", [])

	pricing_rules = [rule["pricing_rule"] for rule in all_rules]

	pricing_rule = None
	if transaction_pricing_rule in pricing_rules:
		pricing_rule = transaction_pricing_rule

	rule_result = {}

	rule_input = {
		"doctype": doc.doctype,
		"transaction_date": doc.transaction_date,
		"company": doc.company,
		"selling_price_list": doc.selling_price_list,
		"total": doc.total,
		"total_qty": doc.total_qty,
		"customer": doc.customer,
		"coupon_code": doc.coupon_code if doc.coupon_code else "",
	}

	rule_result = inno_apply_transaction_pricing_rule(pricing_rule, rule_input)
	doc.additional_discount_percentage = rule_result.get("additional_discount_percentage", 0)
	doc.discount_amount = rule_result.get("discount_amount", 0)
	doc.applied_pricing_rules = rule_result.get("applied_pricing_rules", "[]")
	doc.coupon_pricing_rule_discount_percentage = rule_result.get(
		"coupon_pricing_rule_discount_percentage", 0
	)
	doc.coupon_pricing_rule_discount_amount = rule_result.get("coupon_pricing_rule_discount_amount", 0)

	for free_item in rule_result.get("free_item_data", []):
		item_data = frappe.get_cached_value(
			"Item",
			free_item.get("item_code"),
			["item_name", "description", "stock_uom"],
			as_dict=1,
		)
		free_item_data_args = {
			"item_code": free_item.get("item_code"),
			"qty": free_item.get("qty", 1),
			"rate": free_item.get("rate", 0),
			"price_list_rate": free_item.get("rate", 0),
			"is_free_item": 1,
			"item_name": item_data.item_name,
			"description": item_data.description,
			"uom": free_item.get("uom") or item_data.stock_uom,
			"conversion_factor": get_conversion_factor(
				free_item.get("item_code"),
				free_item.get("uom") or item_data.stock_uom,
			).get("conversion_factor", 1),
			"warehouse": doc.set_warehouse,
			"cost_center": doc.items[0].cost_center
			if doc.items
			else frappe.get_value("Company", doc.company, "default_cost_center"),
			"delivery_date": doc.delivery_date,
		}
		doc.append("items", free_item_data_args)

	doc.set_missing_values(for_validate=True)
	calculate_taxes_and_totals(doc)
	return rule_result


def inno_get_pricing_rule_for_item(item, coupon_code=None):
	if not item.item_code:
		return {
			"price_list_rate": 0,
			"price_or_product_discount": "",
			"pricing_rule_for": "",
			"discount_percentage": 0,
			"discount_amount": 0,
			"rate": 0,
			"free_item_data": [],
			"pricing_rules": "[]",
		}

	item_metadata = frappe.get_value(
		"Omni Item", {"linked_item": item.item_code}, ["stock_uom"], as_dict=True
	)

	selling_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
	price_list_rate = get_price_list_rate_for(
		{
			"customer": "Khách Lẻ",
			"transaction_date": nowdate(),
			"qty": item.qty,
			"uom": item_metadata.stock_uom,
			"price_list": selling_price_list,
		},
		item.item_code,
	)

	item_code = item.item_code

	price_list_rate = price_list_rate or 0.0
	if price_list_rate == 0:
		valuation_rate = frappe.db.get_value("Item", item.item_code, "valuation_rate") or 0
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
					"qty": item.qty,
					"stock_qty": item.qty,
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
			"coupon_code": coupon_code,
		}
	)

	all_rules = get_all_pricing_rules_for_item(args)
	pricing_rule_list = all_rules[0].get("pricing_rules_list", [])
	coupon_rule = all_rules[0].get("coupon_pricing_rules", [])
	pricing_rules = [rule["pricing_rule"] for rule in pricing_rule_list]

	if item.pricing_rule in pricing_rules:
		pricing_rule = item.pricing_rule

	if len(coupon_rule) > 0:
		coupon_rule = coupon_rule[0]["pricing_rule"]

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
			"qty": item.qty,
			"stock_qty": item.qty,
			"uom": item_metadata.get("stock_uom"),
			"price_list_rate": price_list_rate,
			"pricing_rules": frappe.as_json([pricing_rule, coupon_rule]),
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
