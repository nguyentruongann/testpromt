from enum import IntEnum

from pydantic import BaseModel


# Enums for better type safety
class OrderStatus(IntEnum):
	PENDING = 0  # Chưa thanh toán
	PAID = 1  # Đã thanh toán
	# CANCELLED = 2   # Hủy thanh toán đoạn này trong tài liệu nhưng implement trong C# thì không có
	ORDER_IS_CANCELLED = 3  # Đơn hàng đã bị hủy


class PaymentMethod(IntEnum):
	PHYSICAL_CARD = 0  # Thẻ vật lý
	QR_CODE = 2  # QR Code
	GIFT_CARD = 3  # Thẻ quà tặng/Thẻ trả trước


# Base Models
class ResponseData(BaseModel):
	ReturnCode: int
	Description: str


# Order Models
class Product(BaseModel):
	"""Thông tin sản phẩm trong đơn hàng"""

	Name: str
	SKU: str
	MoneyAmount: float
	Size: str | None = None
	Quantity: int
	Unit: str | None = None
	Description: str | None = None

	# VAT fields
	TotalAmountWithoutVAT: float | None = None
	VATPercent: int | None = None
	VATAmount: float | None = None
	TotalAmountWithVAT: float | None = None


class CreateOrderRequest(BaseModel):
	"""Request tạo đơn hàng mới"""

	# Required parameters
	OrderCode: str
	OrderAmount: int
	OrderExpiredDate: str
	AccountName: str
	CreateShopCode: str

	# Optional parameters
	OrderLinkNotify: str | None = None

	# Customer information
	CustomerCode: str | None = None
	CustomerName: str | None = None
	CustomerAddress: str | None = None
	CustomerEmail: str | None = None
	CustomerPhone: str | None = None

	# Product information
	Products: list[Product] | None = None

	# Additional information
	OrderNote: str | None = None
	TerminalID: str | None = None
	PartnerShopCode: str | None = None
	PartnerInfoEx: str | None = None


class GetOrderRequest(BaseModel):
	OrderCode: str
	AccountName: str


class UpdateOrderRequest(BaseModel):
	"""Request cập nhật đơn hàng (hủy đơn)"""

	AccountName: str
	OrderCode: str
	IsCancel: bool


class CreateOrderResponseData(BaseModel):
	"""Dữ liệu response khi tạo đơn hàng thành công"""

	# CreateDate: str
	pass


class CreateOrderResponse(ResponseData):
	"""Response API tạo đơn hàng"""

	ResponseData: CreateOrderResponseData | None = None


class GetOrderResponseData(BaseModel):
	"""Dữ liệu response khi lấy thông tin đơn hàng"""

	ReturnCode: int | None
	OrderCode: str
	OrderAmount: int
	OrderExpireDate: str
	OrderNote: str | None = None
	OrderLinkNotify: str | None = None
	OrderType: int | None = None

	# Customer information
	CustomerName: str | None = None
	CustomerAddress: str | None = None
	CustomerPhone: str | None = None
	CustomerEmail: str | None = None

	# Order status and payment info
	CreateDate: str
	Status: OrderStatus
	PaymentMethodType: PaymentMethod | None = None
	AuthorizationNo: str | None = None
	ReferenceNo: str | None = None

	# Additional payment info that might be included
	PaymentDate: str | None = None
	BankCode: str | None = None
	BankName: str | None = None
	CardNumber: str | None = None
	TransactionID: str | None = None


class GetOrderResponse(ResponseData):
	"""Response API lấy thông tin đơn hàng"""

	ResponseData: GetOrderResponseData | None = None


class UpdateOrderResponse(ResponseData):
	"""Response API cập nhật đơn hàng"""

	pass


# Additional models for webhook notifications
class WebhookNotification(BaseModel):
	"""Thông báo webhook từ Payoo"""

	OrderCode: str
	OrderAmount: int
	Status: OrderStatus
	PaymentDate: str | None = None
	PaymentMethodType: PaymentMethod | None = None
	AuthorizationNo: str | None = None
	ReferenceNo: str | None = None
	BankCode: str | None = None
	TransactionID: str | None = None
	Signature: str


# Error response models
class ErrorResponse(BaseModel):
	"""Response khi có lỗi"""

	ReturnCode: int
	Description: str
	ErrorDetails: str | None = None
