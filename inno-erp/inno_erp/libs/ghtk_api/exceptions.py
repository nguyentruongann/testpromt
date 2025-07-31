class GhtkException(Exception):
	success: bool
	error_code: str | None
	log_id: str | None

	def __init__(
		self, message: str, success: bool = False, error_code: str | None = None, log_id: str | None = None
	):
		super().__init__(message)
		self.success = success
		self.error_code = error_code
		self.log_id = log_id

	def __str__(self):
		return f"GhtkException(success={self.success}, error_code={self.error_code}, log_id={self.log_id}, message={self.args[0]})"


GHTK_FAIL_REASONS = {
	# Delay Picking Up (status_id=8)
	"100": "Shop requests to delay picking up until the next shift",
	"101": "Unable to contact shop owners",
	"102": "Package order is not ready for picking up",
	"103": "Shop changes pick-up address",
	"104": "Shop changes the date of picking-up",
	"105": "Carrier is overloaded",
	"106": "Objective factors (e.g., weather)",
	"107": "Others",
	# Failed to Pick Up (status_id=7)
	"110": "Pick-up address is not supported",
	"111": "Product is not allowed to be delivered (e.g., prohibited products)",
	"112": "Shop requests to cancel order",
	"113": "Over 3 pick-up attempts",
	"114": "Others",
	"115": "Partner requests to cancel order via API",
	# Delay Delivering (status_id=10)
	"120": "Carrier is overloaded",
	"121": "Customer requests to delay until the next shift",
	"122": "Unable to contact customer",
	"123": "Customer requests to receive at another time",
	"124": "Customer changes delivery address",
	"125": "Wrong address; shop needs to double-check",
	"126": "Objective factors (e.g., weather conditions)",
	"127": "Others",
	"128": "Shop changes delivery time",
	"129": "Package is not found",
	"1200": "Wrong contact number; shop needs to double-check",
	# Failed to Deliver (status_id=9)
	"130": "Customer refuses to receive the products",
	"131": "Unable to contact over 3 times",
	"132": "Customer requests to delay over 3 times",
	"133": "Shop requests to cancel order",
	"134": "Others",
	"135": "Partner requests to cancel order via API",
	# Delay Returning (status_id=11)
	"140": "Shop requests to delay until the next shift",
	"141": "Unable to contact shop owners",
	"142": "Shop is not at the returning address",
	"143": "Shop requests to receive the returning order at another time",
	"144": "Others",
}

# Context: GHTK
# 100	Nhà cung cấp (NCC) hẹn lấy vào ca tiếp theo
# 101	GHTK không liên lạc được với NCC
# 102	NCC chưa có hàng
# 103	NCC đổi địa chỉ
# 104	NCC hẹn ngày lấy hàng
# 105	GHTK quá tải, không lấy kịp
# 106	Do điều kiện thời tiết, khách quan
# 107	Lý do khác
# 110	Địa chỉ ngoài vùng phục vụ
# 111	Hàng không nhận vận chuyển
# 112	NCC báo hủy
# 113	NCC hoãn/không liên lạc được 3 lần
# 114	Lý do khác
# 115	Đối tác hủy đơn qua API
# 120	GHTK quá tải, giao không kịp
# 121	Người nhận hàng hẹn giao ca tiếp theo
# 122	Không gọi được cho người nhận hàng
# 123	Người nhận hàng hẹn ngày giao
# 124	Người nhận hàng chuyển địa chỉ nhận mới
# 125	Địa chỉ người nhận sai, cần NCC check lại
# 126	Do điều kiện thời tiết, khách quan
# 127	Lý do khác
# 128	Đối tác hẹn thời gian giao hàng
# 129	Không tìm thấy hàng
# 1200	SĐT người nhận sai, cần NCC check lại
# 130	Người nhận không đồng ý nhận sản phẩm
# 131	Không liên lạc được với KH 3 lần
# 132	KH hẹn giao lại quá 3 lần
# 133	Shop báo hủy đơn hàng
# 134	Lý do khác
# 135	Đối tác hủy đơn qua API
# 140	NCC hẹn trả ca sau
# 141	Không liên lạc được với NCC
# 142	NCC không có nhà
# 143	NCC hẹn ngày trả
# 144	Lý do khác
