from .typing import OrderRequest, OrderResponse, OrderUpdateRequest, TrackingResponse


class ViettelPostOrderApi:
	def __init__(self, client):
		self.client = client

	def create_order(self, order: OrderRequest):
		"""Create a new order with ViettelPost"""
		response = self.client.make_request(
			url="/v2/order/createOrder", method="POST", json=order.model_dump()
		)
		return OrderResponse(**response)

	def update_order(self, order_number: str, update_type: int, note: str = ""):
		"""Update order status"""
		update_request = OrderUpdateRequest(order_number=order_number, update_type=update_type, note=note)

		response = self.client.make_request(
			url="/v2/order/UpdateOrder", method="POST", json=update_request.model_dump()
		)
		return OrderResponse(**response)

	def get_tracking_status(self, order_number: str):
		"""Get order tracking status"""
		response = self.client.make_request(url=f"/v2/order/tracking/{order_number}", method="GET")
		return TrackingResponse(**response)
