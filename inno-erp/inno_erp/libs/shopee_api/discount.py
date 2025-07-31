from .client import ShopeeClient

DISCOUNT_API_PATH = "/api/v2/discount"


class DiscountAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def add_discount(self, discount_name, start_time, end_time):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/add_discount",
			data={
				"discount_name": discount_name,
				"start_time": start_time,
				"end_time": end_time,
			},
		)

	def add_discount_item(self, discount_id, item_list):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/add_discount_item",
			data={
				"discount_id": discount_id,
				"item_list": item_list,
			},
		)

	def delete_discount(self, discount_id):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/delete_discount",
			data={"discount_id": discount_id},
		)

	def delete_discount_item(self, discount_id, item_list):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/delete_discount_item",
			data={"discount_id": discount_id, "item_list": item_list},
		)

	def get_discount(self, discount_id):
		return self.client.make_request(
			"GET",
			f"{DISCOUNT_API_PATH}/get_discount",
			params={"discount_id": discount_id},
		)

	def update_discount(self, discount_id, discount_name, start_time, end_time):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/update_discount",
			data={
				"discount_id": discount_id,
				"discount_name": discount_name,
				"start_time": start_time,
				"end_time": end_time,
			},
		)

	def update_discount_item(self, discount_id, item_list):
		return self.client.make_request(
			"POST",
			f"{DISCOUNT_API_PATH}/update_discount_item",
			data={"discount_id": discount_id, "item_list": item_list},
		)

	def get_discount_list(
		self,
		discount_status="all",
		page_no=1,
		page_size=10,
		update_time_from=None,
		update_time_to=None,
	):
		return self.client.make_request(
			"GET",
			f"{DISCOUNT_API_PATH}/get_discount_list",
			params={
				"discount_status": discount_status,
				"page_no": page_no,
				"page_size": page_size,
				"update_time_from": update_time_from,
				"update_time_to": update_time_to,
			},
		)
