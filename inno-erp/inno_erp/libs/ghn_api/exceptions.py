from typing import Any


class GhnException(Exception):
	code: bool
	message: str
	data: Any | None = None
	code_message: str


GHN_FAIL_REASONS = {
	# Lấy thất bại
	"GHN-PFA1A0": "Người gửi hẹn lại ngày lấy hàng",
	"GHN-PFA2A2": "Thông tin lấy hàng sai (địa chỉ / SĐT)",
	"GHN-PFA2A1": "Thuê bao không liên lạc được / Máy bận",
	"GHN-PFA2A3": "Người gửi không nghe máy",
	"GHN-PFA1A1": "Người gửi muốn gửi hàng tại bưu cục",
	"GHN-PCB0B2": "Hàng vi phạm quy định khối lượng, kích thước",
	"GHN-PFA4A1": "Hàng vi phạm quy cách đóng gói",
	"GHN-PCB0B1": "Người gửi không muốn gửi hàng nữa",
	"GHN-PFA4A2": "Hàng hóa GHN không vận chuyển",
	"GHN-PFA3A2": "Nhân viên gặp sự cố",
	# Giao thất bại
	"GHN-DFC1A0": "Người nhận hẹn lại ngày giao",
	"GHN-DFC1A2": "Không liên lạc được người nhận / Chặn số",
	"GHN-DFC1A4": "Người nhận không nghe máy",
	"GHN-DCD0A1": "Sai thông tin người nhận (địa chỉ / SĐT)",
	"GHN-DFC1A1": "Người nhận đổi địa chỉ giao hàng",
	"GHN-DFC1A7": "Người nhận từ chối nhận do không cho xem / thử hàng",
	"GHN-DCD0A6": "Người nhận từ chối nhận do sai sản phẩm",
	"GHN-DCD0A7": "Người nhận từ chối nhận do sai COD",
	"GHN-DCD0A5": "Người nhận từ chối nhận do hàng hư hỏng",
	"GHN-DCD1A5": "Người nhận từ chối nhận do không có tiền",
	"GHN-DCD0A8": "Người nhận đổi ý không mua nữa",
	"GHN-DCD1A1": "Người nhận báo không đặt hàng",
	"GHN-DFC1A6": "Nhân viên gặp sự cố",
	"GHN-DCD1A3": "Hàng suy suyển, bể vỡ trong quá trình vận chuyển",
	# Trả thất bại
	"GHN-RFE0A0": "Người gửi hẹn lại ngày trả hàng",
	"GHN-RFE0A1": "Người gửi đổi địa chỉ trả hàng",
	"GHN-RFE0A6": "Người gửi không nghe máy",
	"GHN-RFE0A3": "Người gửi từ chối nhận do sai sản phẩm",
	"GHN-RFE0A4": "Người gửi từ chối nhận do hàng hư hỏng",
	"GHN-RFE0A5": "Nhân viên gặp sự cố",
}
