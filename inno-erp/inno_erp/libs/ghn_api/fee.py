from .client import GhnClient
from .typing import (
	GhnAvailableServicesRequest,
	GhnFeeRequest,
)


class GhnFeeApi:
	def __init__(self, client: GhnClient):
		self.client = client

	def get_soc(self, order_code: str) -> dict:
		"""
		Get SOC info for an order.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/soc",
			"POST",
			json={"order_code": order_code},
		)

	def get_fee(self, req: GhnFeeRequest) -> dict:
		"""
		Calculate shipping fee.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/fee",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)

	def get_available_services(self, req: GhnAvailableServicesRequest) -> dict:
		"""
		Get available shipping services.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/available-services",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)
