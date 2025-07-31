from frappe.utils.nestedset import get_descendants_of
from frappe.utils import flt
import frappe
import json


@frappe.whitelist()
def get_items_by_item_groups(item_groups):
	items = []
	for item_group in json.loads(item_groups):
		children = get_descendants_of("Item Group", item_group["item_group"], ignore_permissions=True) + [
			item_group["item_group"]
		]
		items += frappe.get_all(
			"Item",
			filters={"item_group": ("in", children), "has_variants": ("!=", 1)},
			fields=["name", "item_name"],
		)
	return list(map(dict, {tuple(d.items()) for d in items}))


@frappe.whitelist()
def create_multi_item_price(
	reference_method,
	items,
	operator,
	variance,
	value,
	price_list,
	reference_price_list,
	valid_from,
	all_update,
):
	query_current_price = f"""
				SELECT item_code, price_list_rate, name
				FROM (
					SELECT item_code, price_list_rate, name,
						   ROW_NUMBER() OVER (PARTITION BY item_code ORDER BY modified DESC) AS last_price
					FROM `tabItem Price` ip
					where price_list = '{price_list}' and valid_from = '{valid_from}'
				) t
				WHERE last_price = 1
			"""
	current_item_price = frappe.db.sql(query_current_price, as_dict=1)

	if reference_method == "1":
		if not operator or not variance:
			frappe.throw("Vui lòng chọn đủ thông tin!")
		query = f"""
			SELECT item_code, price_list_rate
			FROM (
				SELECT item_code, price_list_rate,
					   ROW_NUMBER() OVER (PARTITION BY item_code ORDER BY modified DESC) AS last_price
				FROM `tabItem Price` ip
				where price_list = '{reference_price_list}'
			) t
			WHERE last_price = 1
		"""
		reference_item_price = frappe.db.sql(query, as_dict=1)
		for item in reference_item_price:
			if operator == "+":
				price_list_rate = (
					item.price_list_rate + (item.price_list_rate * flt(value) / 100)
					if variance == "%"
					else item.price_list_rate + flt(value)
				)
			else:
				price_list_rate = (
					item.price_list_rate - (item.price_list_rate * flt(value) / 100)
					if variance == "%"
					else item.price_list_rate - flt(value)
				)
			check = False
			for current_item in current_item_price:
				if current_item.item_code == item.item_code:
					check = True
					if all_update != "1":
						frappe.db.set_value(
							"Item Price",
							current_item.name,
							{
								"price_list_rate": price_list_rate,
								"valid_from": valid_from,
							},
						)
					break
			if check:
				continue
			item_price = frappe.new_doc("Item Price")
			item_price.item_code = item.item_code
			item_price.price_list = price_list
			item_price.valid_from = valid_from
			item_price.price_list_rate = price_list_rate
			item_price.insert(ignore_permissions=True)
	else:
		items = eval(items)
		for item in items:
			check = False
			for current_item in current_item_price:
				if current_item.item_code == item["item_code"]:
					check = True
					frappe.db.set_value(
						"Item Price",
						current_item.name,
						{
							"price_list_rate": flt(item["rate"]) if "rate" in item else 0,
							"valid_from": valid_from,
						},
					)
					break
			if check:
				continue
			item_price = frappe.new_doc("Item Price")
			item_price.item_code = item["item_code"]
			item_price.price_list = price_list
			item_price.valid_from = valid_from
			item_price.price_list_rate = flt(item["rate"]) if "rate" in item else 0
			item_price.insert(ignore_permissions=True)
