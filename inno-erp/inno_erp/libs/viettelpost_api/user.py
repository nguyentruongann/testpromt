from .typing import InventoryResponse


class ViettelPostUserApi:
	def __init__(self, client):
		self.client = client

	def list_inventory(self):
		"""Get list of user inventory/addresses"""
		response = self.client.make_request(url="/v2/user/listInventory", method="GET")
		return InventoryResponse(**response)
