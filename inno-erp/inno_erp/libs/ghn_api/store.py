from .client import GhnClient
from .typing import GhnStoreResponse


class GhnStoreApi:
	def __init__(self, client: GhnClient):
		self.client = client

	def getAllStore(
		self, client_phone: str | None = None, offset: int = 0, limit: int = 200
	) -> GhnStoreResponse:
		params = {"offset": offset, "limit": limit}
		if client_phone:
			params["client_phone"] = client_phone

		response = self.client.make_request(
			"/shiip/public-api/v2/shop/all",
			"GET",
			params=params,
		)
		return GhnStoreResponse(**response)
