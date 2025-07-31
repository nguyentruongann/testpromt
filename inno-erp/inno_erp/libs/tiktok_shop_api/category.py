import time

from .client import TiktokShopClient

# from .config import Config
from .typing.category import TiktokShopCategoryRulesResponse, TiktokShopGetCategoriesResponse


class TiktokShopCategoryAPI:
	def __init__(self, client: TiktokShopClient):
		self.client = client

	# def get_categories(self, shop_cipher: str, locale: str = None) -> TiktokShopGetCategoriesResponse:
	# 	params = {"shop_cipher": shop_cipher}
	# 	if locale:
	# 		params["locale"] = locale
	# 	return self.client.make_request("GET", Config.API_MAP["GET_CATEGORIES"], params=params)

	# def get_category_rules(self, shop_cipher, category_id, locale="vi-VN"):
	# 	params = {"shop_cipher": shop_cipher, "locale": locale, "timestamp": int(time.time())}
	# 	url = Config.API_MAP["GET_CATEGORY_RULES"]
	# 	return self.client.make_request("GET", f"{url}/{category_id}/rules", params=params)
