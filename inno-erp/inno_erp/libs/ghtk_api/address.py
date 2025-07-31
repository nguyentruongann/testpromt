from .client import GhtkClient
from .typing import Address4LevelRequest, Address4LevelResponse, PickAddResponse


class GhtkAddressApi:
	def __init__(self, client: GhtkClient):
		self.client = client

	def getAddressLevel4(self, address: Address4LevelRequest) -> Address4LevelResponse:
		response = self.client.make_request(
			"/services/address/getAddressLevel4",
			"GET",
			params=address.model_dump(),
		)
		return Address4LevelResponse(**response)

	def getListPickAdd(self) -> PickAddResponse:
		response = self.client.make_request(
			"/services/shipment/list_pick_add",
			"GET",
		)
		return PickAddResponse(**response)
