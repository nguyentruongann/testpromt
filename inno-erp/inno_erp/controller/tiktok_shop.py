from copy import copy

import frappe
from frappe import _

from inno_erp.libs.tiktok_shop_api import TiktokShopApi
from inno_erp.libs.tiktok_shop_api.auth import TiktokShopAuthApi


@frappe.whitelist(allow_guest=True)
def oauth_callback(app_key: str, code: str, locale: str | None = None, shop_region: str | None = None):
	tiktok_shop_conf = frappe.conf.get("tiktok_shop")
	if app_key != tiktok_shop_conf.get("app_key"):
		frappe.throw(_("Failed to authorize"))

	client = TiktokShopAuthApi(tiktok_shop_conf.get("app_key"), tiktok_shop_conf.get("app_secret"))
	response = client.get_access_token(code)
	token = response.data

	api = TiktokShopApi(
		access_token=token.access_token,
		app_key=tiktok_shop_conf.get("app_key"),
		app_secret=tiktok_shop_conf.get("app_secret"),
	)

	authorized_shops = api.shop.get_authorized_shop()
	active_shops = api.shop.get_active_shops()

	active_shop_ids = [shop.id for shop in active_shops.shops]

	for shop in authorized_shops.shops:
		shop_token = copy(token)
		shop_token.cipher = shop.cipher

		exist_shops = frappe.db.get_all("Omni Shop", filters={"platform": "Tiktok Shop", "shop_id": shop.id})
		if exist_shops:
			frappe.db.set_value(
				"Omni Shop",
				exist_shops[0].name,
				{
					"credentials": shop_token.model_dump_json(),
					"shop_name": shop.name,
					"shop_id": shop.id,
					"seller_id": shop.id,
					"disabled": shop.id not in active_shop_ids,
				},
			)
			continue

		new_shop = frappe.get_doc(
			{
				"doctype": "Omni Shop",
				"credentials": shop_token.model_dump_json(),
				"shop_name": shop.name,
				"platform": "Tiktok Shop",
				"shop_id": shop.id,
				"seller_id": shop.id,
				"disabled": shop.id not in active_shop_ids,
			},
		)
		new_shop.insert(ignore_permissions=True)

	frappe.db.commit()
	frappe.local.response["type"] = "redirect"
	frappe.local.response["location"] = "/tab_close.html"


@frappe.whitelist(allow_guest=True)
def callback(**kwargs):
	print(kwargs)
	return "OK"
