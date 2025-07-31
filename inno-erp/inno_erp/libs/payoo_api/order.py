from .client import PayooMPOSAPIClient
from .typing import (
	CreateOrderRequest,
	CreateOrderResponse,
	GetOrderRequest,
	GetOrderResponse,
	UpdateOrderRequest,
	UpdateOrderResponse,
)


class PayooOrderAPI:
	"""
	Cung cấp các phương thức tương tác với Order API của Payoo.
	"""

	def __init__(self, client: PayooMPOSAPIClient):
		self.client = client

	def create(self, order_data: CreateOrderRequest) -> CreateOrderResponse:
		response = self.client.post("CreateOrderV2", order_data)
		return CreateOrderResponse(**response)

	def get(self, order_code: str) -> GetOrderResponse:
		req_model = GetOrderRequest(AccountName=self.client.account_name, OrderCode=order_code)
		response_json = self.client.post("GetOrder", req_model)
		return GetOrderResponse.model_validate(response_json)

	def cancel(self, order_code: str) -> UpdateOrderResponse:
		req_model = UpdateOrderRequest(
			AccountName=self.client.account_name,
			OrderCode=order_code,
			IsCancel=True,
			# OrderCode=order_code, IsCancel=True
		)
		response_json = self.client.post("UpdateOrder", req_model)
		return UpdateOrderResponse.model_validate(response_json)
