from .client import GhtkClient
from .typing import FeeRequest, FeeResponse, OrderRequest, OrderSuccess, TrackingStatusResponse


class GhtkOrderAPI:
	def __init__(self, client: GhtkClient):
		self.client = client

	def create_order(self, order: OrderRequest):
		response = self.client.make_request(
			"/services/shipment/order",
			"POST",
			json=order.model_dump(exclude_none=True),
		)
		return OrderSuccess(**response)

	def calculate_fee(self, fee: FeeRequest):
		response = self.client.make_request(
			"/services/shipment/fee",
			"GET",
			params=fee.model_dump(exclude_none=True),
		)
		return FeeResponse(**response)

	def get_tracking_status(self, order_id: str):
		response = self.client.make_request(
			f"/services/shipment/v2/{order_id}",
			"GET",
		)
		return TrackingStatusResponse(**response)
