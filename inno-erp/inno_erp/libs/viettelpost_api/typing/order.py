from pydantic import BaseModel

from .auth import ViettelPostResponse


class OrderItem(BaseModel):
	product_name: str
	product_price: float
	product_weight: int  # in grams
	product_quantity: int


class OrderRequest(BaseModel):
	# Sender information
	sender_fullname: str
	sender_address: str
	sender_phone: str
	sender_email: str | None = None

	# Receiver information
	receiver_fullname: str
	receiver_address: str
	receiver_phone: str
	receiver_email: str | None = None

	# Order details
	product_type: str = "HH"  # Default to goods
	order_payment: int = 3  # Default payment method
	order_service: str = "STK"  # Default service
	order_service_add: str = ""
	order_voucher: str = ""
	order_note: str = ""

	# Money details
	money_collection: float = 0  # COD amount
	money_totalfee: float = 0
	money_feecod: float = 0
	money_feevas: float = 0
	money_feeinsurrance: float = 0
	money_fee: float = 0
	money_feeother: float = 0
	money_totalvat: float = 0
	money_total: float = 0

	# Items
	list_item: list[OrderItem]

	# Optional delivery date
	delivery_date: str | None = None


class OrderUpdateRequest(BaseModel):
	order_number: str
	update_type: int  # 1=Confirm, 2=Return, 3=Redeliver, 4=Cancel, 5=Reorder, 11=Delete
	note: str = ""


class OrderData(BaseModel):
	order_number: str
	money_collection: float
	exchange_weight: int
	money_total: float
	money_total_fee: float
	money_fee: float
	money_collection_fee: float
	money_other_fee: float
	money_vas: float
	money_vat: float
	kpi_ht: float
	receiver_province: int | None = None
	receiver_district: int | None = None
	receiver_wards: int | None = None


class OrderResponse(ViettelPostResponse):
	data: OrderData | None = None


class TrackingStatus(BaseModel):
	order_number: str
	status: str | None = None
	status_text: str | None = None
	created: str | None = None
	modified: str | None = None
	message: str | None = None
	customer_name: str | None = None
	customer_phone: str | None = None
	address: str | None = None


class TrackingResponse(ViettelPostResponse):
	data: TrackingStatus | None = None

	# Money details
	money_collection: float = 0  # COD amount
	money_totalfee: float = 0
	money_feecod: float = 0
	money_feevas: float = 0
	money_feeinsurrance: float = 0
	money_fee: float = 0
	money_feeother: float = 0
	money_totalvat: float = 0
	money_total: float = 0

	# Items
	list_item: list[OrderItem]

	# Optional delivery date
	delivery_date: str | None = None


class OrderUpdateRequest(BaseModel):
	order_number: str
	update_type: int  # 1=Confirm, 2=Return, 3=Redeliver, 4=Cancel, 5=Reorder, 11=Delete
	note: str = ""

	# Money details
	money_collection: float = 0  # COD amount
	money_totalfee: float = 0
	money_feecod: float = 0
	money_feevas: float = 0
	money_feeinsurrance: float = 0
	money_fee: float = 0
	money_feeother: float = 0
	money_totalvat: float = 0
	money_total: float = 0

	# Items
	list_item: list[OrderItem] | None = None

	# Optional delivery date
	delivery_date: str | None = None
