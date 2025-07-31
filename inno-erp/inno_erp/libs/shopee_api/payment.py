from .client import ShopeeClient

PAYMENT_API_PATH = "/api/v2/payment"


class PaymentAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_escrow_detail(
		self,
		order_sn,
	):
		return self.client.make_request(
			"GET",
			f"{PAYMENT_API_PATH}/get_escrow_detail",
			params={"order_sn": order_sn},
		)
