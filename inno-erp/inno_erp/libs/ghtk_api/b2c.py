from .client import GhtkClient
from .typing import ShopLoginRequest, ShopRequest, ShopResponse


class GhtkB2CApi:
	def __init__(self, client: GhtkClient):
		self.client = client

	def create_shop(self, shop: ShopRequest):
		response = self.client.make_request(
			"/services/shops/add",
			"POST",
			json=shop.model_dump(),
		)
		return ShopResponse(**response)

	def get_shop_token(self, shop: ShopLoginRequest):
		response = self.client.make_request(
			"/services/shops/token",
			"POST",
			json=shop.model_dump(),
		)
		return ShopResponse(**response)
