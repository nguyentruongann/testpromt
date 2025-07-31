from .client import TiktokShopClient
from .typing import TiktokShopActiveShopResponse, TiktokShopAuthorizedShopResponse


class TiktokShopShopAPI:
	def __init__(self, client: TiktokShopClient):
		self.client = client

	def get_authorized_shop(self):
		response = self.client.make_request("/authorization/202309/shops", method="GET")
		return TiktokShopAuthorizedShopResponse(**response["data"])

	def get_active_shops(self):
		response = self.client.make_request("/seller/202309/shops", method="GET")
		return TiktokShopActiveShopResponse(**response["data"])
