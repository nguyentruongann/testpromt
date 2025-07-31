from .client import ShopeeClient

LOGISTICS_API_PATH = "/api/v2/logistics"


class LogisticsAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	# Lấy thông tin cần thiết để tạo đơn vận chuyển.
	def get_shipping_parameter(self, order_sn, package_number):
		return self.client.make_request(
			"GET",
			f"{LOGISTICS_API_PATH}/get_shipping_parameter",
			params={"order_sn": order_sn, "package_number": package_number},
		)

	# Xác nhận giao hàng cho đơn hàng cụ thể.
	def ship_order(self, order_sn, package_number, pickup):
		return self.client.make_request(
			"POST",
			f"{LOGISTICS_API_PATH}/ship_order",
			data={
				"order_sn": order_sn,
				"package_number": package_number,
				"pickup": pickup,
			},
		)

	# Cập nhật nhãn vận chuyển cho đơn hàng.
	def update_shipping_label(self, order_sn, package_number):
		return self.client.make_request(
			"POST",
			f"{LOGISTICS_API_PATH}/update_shipping_label",
			data={
				"order_sn": order_sn,
				"package_number": package_number,
			},
		)

	# Lấy mã vận đơn cho đơn hàng.
	def get_tracking_number(self, order_sn, package_number):
		return self.client.make_request(
			"GET",
			f"{LOGISTICS_API_PATH}/get_tracking_number",
			params={"order_sn": order_sn, "package_number": package_number},
		)

	#  Lấy thông tin theo dõi đơn hàng
	def get_tracking_info(self, order_sn, package_number):
		return self.client.make_request(
			"GET",
			f"{LOGISTICS_API_PATH}/get_tracking_info",
			params={"order_sn": order_sn, "package_number": package_number},
		)
