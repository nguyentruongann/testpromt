from .client import ShopeeClient

ORDER_API_PATH = "/api/v2/order"


class OrderAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_order_list(
		self,
		time_range_field,
		time_from,
		time_to,
		page_size,
		cursor,
	):
		return self.client.make_request(
			"GET",
			f"{ORDER_API_PATH}/get_order_list",
			params={
				"time_range_field": time_range_field,
				"time_from": time_from,
				"time_to": time_to,
				"page_size": page_size,
				"cursor": cursor,
			},
		)

	def get_order_detail(
		self,
		order_sn_list,
		request_order_status_pending,
		response_optional_fields,
	):
		return self.client.make_request(
			"GET",
			f"{ORDER_API_PATH}/get_order_detail",
			params={
				"order_sn_list": order_sn_list,
				"request_order_status_pending": request_order_status_pending,
				"response_optional_fields": response_optional_fields,
			},
		)

	def cancel_order(self, order_sn, cancel_reason, item_id, model_id):
		item_list = [{"item_id": item_id, "model_id": model_id}]

		data = {
			"order_sn": order_sn,
			"cancel_reason": cancel_reason,
			"item_list": item_list,
		}

		return self.client.make_request("POST", f"{ORDER_API_PATH}/cancel_order", data=data)
