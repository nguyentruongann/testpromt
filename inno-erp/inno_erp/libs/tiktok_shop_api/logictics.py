from .client import TiktokShopClient


class TiktokShopLogisticsAPI:
	def __init__(self, client: TiktokShopClient):
		"""Khởi tạo TikTokProduct với TikTokClient."""
		self.client = client

	# def get_warehouse_list(self, shop_cipher: str, locale: str = None):
	# 	params = {"shop_cipher": shop_cipher}
	# 	if locale:
	# 		params["locale"] = locale
	# 	return self.client.make_request("GET", Config.API_MAP["GET_WAREHOUSE_LIST"], params=params)
