from .client import ShopeeClient

VOUCHER_API_PATH = "/api/v2/voucher"


class VoucherAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_voucher_list(self, page_no, page_size, status="all"):
		return self.client.make_request(
			"GET",
			f"{VOUCHER_API_PATH}/get_voucher_list",
			params={
				"page_no": page_no,
				"page_size": page_size,
				"status": status,
			},
		)

	def get_voucher_detail(self, voucher_id):
		return self.client.make_request(
			"GET",
			f"{VOUCHER_API_PATH}/get_voucher",
			params={"voucher_id": voucher_id},
		)

	def add_voucher(self, voucher_data):
		return self.client.make_request(
			"POST",
			f"{VOUCHER_API_PATH}/add_voucher",
			data=voucher_data,
		)

	def update_voucher(self, voucher_id, voucher_data):
		return self.client.make_request(
			"POST",
			f"{VOUCHER_API_PATH}/update_voucher",
			data=voucher_data,
		)

	def delete_voucher(self, voucher_id):
		return self.client.make_request(
			"POST",
			f"{VOUCHER_API_PATH}/delete_voucher",
			data={"voucher_id": voucher_id},
		)

	def end_voucher(self, voucher_id):
		return self.client.make_request(
			"POST",
			f"{VOUCHER_API_PATH}/end_voucher",
			data={"voucher_id": voucher_id},
		)
