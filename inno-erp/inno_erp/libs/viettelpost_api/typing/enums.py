from enum import Enum, IntEnum


class OrderStatus(IntEnum):
	"""Order status codes"""

	PENDING = 1
	CONFIRMED = 2
	PICKED_UP = 3
	IN_TRANSIT = 4
	DELIVERED = 5
	RETURNED = 6
	CANCELLED = 7


class OrderUpdateType(IntEnum):
	"""Order update type codes"""

	CONFIRM = 1
	CONFIRM_RETURN_SHIPPING = 2
	REDELIVER = 3
	CANCEL = 4
	REORDER = 5
	DELETE_CANCELLED = 11


class ProductType(Enum):
	"""Product type codes"""

	GOODS = "HH"  # Hàng hóa
	DOCUMENTS = "TL"  # Tài liệu


class PaymentMethod(IntEnum):
	"""Payment method codes"""

	SENDER_PAYS = 1
	RECEIVER_PAYS = 2
	THIRD_PARTY_PAYS = 3


class NationalType(IntEnum):
	"""National delivery type"""

	DOMESTIC = 1
	INTERNATIONAL = 2


class ServiceCode(Enum):
	"""Main service codes"""

	# Standard services
	ROAD_TRANSPORT = "VCBO"  # Chuyển phát đường bộ
	ECONOMY = "STK"  # Chuyển phát tiết kiệm
	HEAVY_ECONOMY = "BTK"  # Hàng nặng tiết kiệm
	HEAVY_FAST = "BCN"  # Hàng nặng nhanh
	AIR_TRANSPORT = "VCBA"  # Chuyển phát đường bay
	COLD_TRANSPORT = "VHL"  # Chuyển phát hàng lạnh
	EXPRESS = "SHT"  # Chuyển phát hỏa tốc
	FAST = "SCN"  # Chuyển phát nhanh

	# COD services
	COD_FAST = "SCOD"  # COD Liên tỉnh nhanh
	COD_ECONOMY = "ECOD"  # COD Liên tỉnh tiết kiệm

	# E-commerce services
	ECOMMERCE_FAST = "NCOD"  # TMĐT nhanh thỏa thuận
	ECOMMERCE_ECONOMY = "LCOD"  # TMĐT tiết kiệm thỏa thuận

	# Provincial services
	PROVINCIAL_FAST = "PTN"  # Nội tỉnh nhanh thỏa thuận
	PROVINCIAL_ECONOMY = "PHS"  # Nội tỉnh tiết kiệm thỏa thuận

	# Agreement services
	FAST_AGREEMENT = "VCN"  # CP nhanh thỏa thuận
	ECONOMY_AGREEMENT = "VTK"  # CP tiết kiệm thỏa thuận
	EXPRESS_AGREEMENT = "VHT"  # Hỏa tốc thỏa thuận

	# Special commitment services
	COMMITMENT_01 = "VSL1"  # Cam kết sản lượng 01
	COMMITMENT_02 = "VSL2"  # Cam kết sản lượng 02
	COMMITMENT_03 = "VSL3"  # Cam kết sản lượng 03
	COMMITMENT_04 = "VSL4"  # Flashsale Tết
	COMMITMENT_05 = "VSL5"  # Cam kết sản lượng 05
	COMMITMENT_06 = "VSL6"  # Cam kết sản lượng 06
	COMMITMENT_07 = "VSL7"  # Cam kết sản lượng 07
	COMMITMENT_08 = "VSL8"  # Cam kết sản lượng 08
	FLASHSALE = "VSL9"  # Flashsale thỏa thuận


class ExtraServiceCode(Enum):
	"""Extra service codes"""

	# Delivery services
	POST_OFFICE_DELIVERY = "GGD"  # Giao Bưu phẩm tại điểm giao dịch
	FORWARD_DELIVERY = "GCTP"  # Chuyển tiếp
	DELIVERY_NOTICE = "GBP"  # Báo phát
	HAND_DELIVERY = "GTT"  # Phát tận tay
	INSPECTION = "GDK"  # Đồng kiểm
	POST_OFFICE_PICKUP = "GNG"  # Gửi hàng tại bưu cục
	BOX_PICKUP = "NBOX"  # Nhận hàng tại Box
	PARTIAL_DELIVERY = "GG1P"  # Giao Một Phần
	SPECIAL_DELIVERY = "GST"  # Giao hàng đặc thù

	# Value and insurance services
	DECLARED_VALUE = "GBH"  # Khai giá
	CASH_ON_INSPECTION = "XMG"  # Thu tiền xem hàng

	# Return services
	TWO_WAY_RETURN = "TRS"  # Hoàn cước hai chiều
	RETURN_SHIPPING = "RRS"  # Hoàn cước chiều về
	FORWARD_RETURN = "FRS"  # Hoàn cước chiều đi
	EXCHANGE_GOODS = "GGDH"  # Đổi hàng
	INTERNAL_EXCHANGE = "GDH"  # Đổi Trả Hàng Nội Bộ

	# Packaging services
	REINFORCEMENT = "GGC"  # Gia cố hàng hóa

	# Notification services
	SMS_NOTIFICATION = "SMS"  # SMS thông báo đơn hàng
	ZALO_NOTIFICATION = "ZNS"  # Zalo thông báo đơn hàng

	# Special cargo services
	HIGH_VALUE = "HGC"  # Hàng giá trị cao
	FRAGILE = "HDV"  # Hàng dễ vỡ
	DOCUMENTS = "HDN"  # Hóa đơn, giấy chứng nhận
	OVERSIZED = "HQK"  # Hàng quá khổ
	BULK_CARGO = "HNK"  # Hàng nguyên khối
	LIQUID = "HCL"  # Chất lỏng
	MAGNETIC_BATTERY = "HPN"  # Hàng từ tính, pin
