from .client import GhnClient
from .typing import (
	GhnCreateOrderRequest,
	GhnLeadtimeRequest,
	GhnPreviewOrderRequest,
	GhnUpdateCODRequest,
	GhnUpdateOrderRequest,
)


class GhnOrderApi:
	def __init__(self, client: GhnClient):
		self.client = client

	def create_shipping_order(self, req: GhnCreateOrderRequest) -> dict:
		"""
		Create a new shipping order.
		:param req: GhnCreateOrderRequest
		:return: API response dict
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/create",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)

	def update_shipping_order(self, req: GhnUpdateOrderRequest) -> dict:
		"""
		Update an existing shipping order's note.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/update",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)

	def cancel_order(self, order_codes: list[str]) -> dict:
		"""
		Cancel one or more orders.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/switch-status/cancel",
			"POST",
			json={"order_codes": order_codes},
		)

	def return_order(self, order_codes: list[str]) -> dict:
		"""
		Mark one or more orders as return.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/switch-status/return",
			"POST",
			json={"order_codes": order_codes},
		)

	def generate_a5_token(self, order_codes: list[str]) -> dict:
		"""
		Generate A5 token for one or more orders.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/a5/gen-token",
			"POST",
			json={"order_codes": order_codes},
		)

	def get_order_detail(self, order_codes: list[str]) -> dict:
		"""
		Get detail of a shipping order.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/detail",
			"POST",
			json={"order_codes": order_codes},
		)

	def switch_status_storing(self, order_codes: list[str]) -> dict:
		"""
		Mark one or more orders as storing.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/switch-status/storing",
			"POST",
			json={"order_codes": order_codes},
		)

	def update_cod_amount(self, req: GhnUpdateCODRequest) -> dict:
		"""
		Update COD amount for an order.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/updateCOD",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)

	def get_leadtime(self, req: GhnLeadtimeRequest) -> dict:
		"""
		Get leadtime for a shipping order.
		"""
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/leadtime",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)

	def preview_shipping_order(self, req: GhnPreviewOrderRequest) -> dict:
		return self.client.make_request(
			"/shiip/public-api/v2/shipping-order/preview",
			"POST",
			json=req.model_dump_json(exclude_none=True),
		)
