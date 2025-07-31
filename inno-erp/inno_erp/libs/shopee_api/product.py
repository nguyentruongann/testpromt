from .client import ShopeeClient

PRODUCT_API_PATH = "/api/v2/product"


class ProductAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_category(self):
		return self.client.make_request(
			"GET",
			f"{PRODUCT_API_PATH}/get_category",
		)

	def get_item_list(self, page_size=10, offset=0, item_status="NORMAL"):
		return self.client.make_request(
			"GET",
			f"{PRODUCT_API_PATH}/get_item_list",
			params={
				"page_size": page_size,
				"offset": offset,
				"item_status": item_status,
			},
		)

	def get_item_base_info(self, item_id_list):
		return self.client.make_request(
			"GET",
			f"{PRODUCT_API_PATH}/get_item_base_info",
			params={"item_id_list": ",".join(map(str, item_id_list))},
		)

	def add_item(self, item_data):
		return self.client.make_request(
			"POST",
			f"{PRODUCT_API_PATH}/add_item",
			data=item_data,
		)

	def update_item(self, item_id, item_data):
		return self.client.make_request(
			"POST",
			f"{PRODUCT_API_PATH}/update_item",
			data=item_data,
			params={"item_id": item_id},
		)

	def delete_item(self, item_id):
		return self.client.make_request(
			"POST",
			f"{PRODUCT_API_PATH}/delete_item",
			params={"item_id": item_id},
		)
