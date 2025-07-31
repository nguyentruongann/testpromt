import frappe
from frappe.utils.caching import redis_cache

from inno_erp.libs.lazada_api import LazadaAPI
from inno_erp.libs.lazada_api.auth import LazadaAuthApi
from inno_erp.libs.lazada_api.typing import *


@frappe.whitelist(allow_guest=True)
def oauth_callback(code: str):
	app_key = frappe.conf.get("lazada").get("app_key")
	app_secret = frappe.conf.get("lazada").get("app_secret")

	client = LazadaAuthApi(app_key, app_secret)
	response = client.get_access_token(code)

	api = LazadaAPI(
		response.access_token,
		app_key,
		app_secret,
	)
	result = api.seller.get_seller_info()
	seller_info = result.data

	exist_shops = frappe.db.get_all(
		"Omni Shop", filters={"platform": "Lazada", "shop_id": seller_info.short_code}
	)

	if exist_shops:
		frappe.db.set_value(
			"Omni Shop",
			exist_shops[0].name,
			{
				"credentials": response.model_dump_json(),
				"shop_name": seller_info.name,
				"shop_id": seller_info.short_code,
				"seller_id": seller_info.seller_id,
				"image": seller_info.logo_url,
			},
		)
	else:
		new_shop = frappe.get_doc(
			{
				"doctype": "Omni Shop",
				"platform": "Lazada",
				"credentials": response.model_dump_json(),
				"shop_name": seller_info.name,
				"shop_id": seller_info.short_code,
				"seller_id": seller_info.seller_id,
				"image": seller_info.logo_url,
			}
		)
		new_shop.insert(ignore_permissions=True)

	frappe.db.commit()
	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = "/tab_close.html"


@frappe.whitelist(allow_guest=True)
def callback(**kwargs):
	print(kwargs)
	return "OK"


@frappe.whitelist(allow_guest=True)
@redis_cache(user=False)
def get_category_tree():
	app_key = frappe.conf.get("lazada").get("app_key")
	app_secret = frappe.conf.get("lazada").get("app_secret")

	api = LazadaAPI(
		"",
		app_key=app_key,
		app_secret=app_secret,
	)

	category_tree = api.product.get_category_tree(language_code="vi_VN").model_dump()["data"]
	return flat_category_tree_recursive(category_tree)


def flat_category_tree_recursive(category_tree, parent_id: int | None = None):
	flat_categories = []
	for category in category_tree:
		flat_categories.append(
			{"label": category.get("name"), "value": category.get("category_id"), "parent_id": parent_id}
		)
		children = category.get("children", [])
		if children:
			flat_categories.extend(flat_category_tree_recursive(children, category.get("category_id")))
	return flat_categories
