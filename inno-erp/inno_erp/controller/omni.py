import frappe

BASE_URLS = {
	"LAZADA": "https://auth.lazada.com/oauth/authorize",
	"TIKTOK_SHOP": "https://services.tiktokshop.com/open/authorize",
	"SHOPEE": "https://auth.shopee.com/oauth/authorize",
}


@frappe.whitelist(allow_guest=True)
def oauth_authorize(platform: str):
	"""Generate Lazada authorization URL"""
	import urllib.parse

	if platform == "LAZADA":
		# redirect_uri = frappe.utils.get_url("/api/method/inno_erp.controller.lazada.oauth_callback")
		redirect_uri = (
			"https://630290d90528.ngrok-free.app/api/method/inno_erp.controller.lazada.oauth_callback"
		)
		params = {
			"client_id": frappe.conf.get("lazada").get("app_key"),
			"response_type": "code",
			"redirect_uri": redirect_uri,
			"force_auth": "true",
		}
		return f"{BASE_URLS['LAZADA']}?{urllib.parse.urlencode(params)}"

	if platform == "TIKTOK_SHOP":
		# 	"https://630290d90528.ngrok-free.app/api/method/inno_erp.controller.tiktok_shop.oauth_callback"
		tiktok_shop_conf = frappe.conf.get("tiktok_shop")
		params = {"service_id": tiktok_shop_conf.get("service_id")}
		return f"{BASE_URLS['TIKTOK_SHOP']}?{urllib.parse.urlencode(params)}"

	return False
