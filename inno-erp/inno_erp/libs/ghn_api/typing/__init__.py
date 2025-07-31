from pydantic import BaseModel, Field

# Please keep __all__ alphabetized within each category.
__all__ = ["GhnResponse", "OrderStatusWebhook"]


class GhnResponse(BaseModel):
	code: int
	message: str | None = None


class GhnFeeWebhook(BaseModel):
	CODFailedFee: int | None = None
	CODFee: int | None = None
	Coupon: int | None = None
	DeliverRemoteAreasFee: int | None = None
	DocumentReturn: int | None = None
	DoubleCheck: int | None = None
	Insurance: int | None = None
	MainService: int | None = None
	PickRemoteAreasFee: int | None = None
	R2S: int | None = None
	Return: int | None = None
	StationDO: int | None = None
	StationPU: int | None = None
	Total: int | None = None


class OrderStatusWebhook(BaseModel):
	CODAmount: int | None = None
	CODTransferDate: str | None = None
	ClientOrderCode: str | None = None
	ConvertedWeight: int | None = None
	Description: str | None = None
	Fee: GhnFeeWebhook | None = None
	Height: int | None = None
	IsPartialReturn: bool | None = None
	Length: int | None = None
	OrderCode: str | None = None
	PartialReturnCode: str | None = None
	PaymentType: int | None = None
	Reason: str | None = None
	ReasonCode: str | None = None
	ShopID: int | None = None
	Status: str | None = None
	Time: str | None = None
	TotalFee: int | None = None
	Type: str | None = None
	Warehouse: str | None = None
	Weight: int | None = None
	Width: int | None = None


class GhnStore(BaseModel):
	id: int = Field(..., alias="_id")
	name: str | None = None
	phone: str | None = None
	address: str | None = None
	ward_code: str | None = None
	district_id: int | None = None
	client_id: int | None = None
	bank_account_id: int | None = None
	status: int | None = None
	location: dict | None = None
	version_no: str | None = None
	is_created_chat_channel: bool | None = None
	address_v2: str | None = None
	ward_id_v2: int | None = None
	province_id_v2: int | None = None
	is_new_address: bool | None = None
	updated_ip: str | None = None
	updated_employee: int | None = None
	updated_client: int | None = None
	updated_source: str | None = None
	updated_date: str | None = None
	created_ip: str | None = None
	created_employee: int | None = None
	created_client: int | None = None
	created_source: str | None = None
	created_date: str | None = None


class GhnStoreData(BaseModel):
	last_offset: int
	shops: list[GhnStore] | None = None


class GhnStoreResponse(GhnResponse):
	data: GhnStoreData | None = None


__all__ += ["GhnStoreResponse"]

# --- GHN API Request Models ---


class GhnCreateOrderItemCategory(BaseModel):
	level1: str | None = None


class GhnCreateOrderItem(BaseModel):
	name: str
	code: str | None = None
	quantity: int
	price: int | None = None
	length: int | None = None
	width: int | None = None
	height: int | None = None
	weight: int | None = None
	category: GhnCreateOrderItemCategory | None = None


class GhnCreateOrderRequest(BaseModel):
	payment_type_id: int
	note: str | None = None
	required_note: str | None = None
	from_name: str | None = None
	from_phone: str | None = None
	from_address: str | None = None
	from_ward_name: str | None = None
	from_district_name: str | None = None
	from_province_name: str | None = None
	return_phone: str | None = None
	return_address: str | None = None
	return_district_id: int | None = None
	return_ward_code: str | None = None
	client_order_code: str | None = None
	to_name: str | None = None
	to_phone: str | None = None
	to_address: str | None = None
	to_ward_code: str | None = None
	to_district_id: int | None = None
	cod_amount: int | None = None
	content: str | None = None
	weight: int | None = None
	length: int | None = None
	width: int | None = None
	height: int | None = None
	pick_station_id: int | None = None
	deliver_station_id: int | None = None
	insurance_value: int | None = None
	service_id: int | None = None
	service_type_id: int | None = None
	coupon: str | None = None
	pick_shift: list[int] | None = None
	items: list[GhnCreateOrderItem] | None = None


class GhnUpdateOrderRequest(BaseModel):
	order_code: str
	note: str | None = None


class GhnUpdateCODRequest(BaseModel):
	order_code: str
	cod_amount: int


class GhnLeadtimeRequest(BaseModel):
	from_district_id: int
	from_ward_code: str
	to_district_id: int
	to_ward_code: str
	service_id: int


class GhnPreviewOrderItemCategory(BaseModel):
	level1: str | None = None


class GhnPreviewOrderItem(BaseModel):
	name: str
	code: str | None = None
	quantity: int
	price: int | None = None
	length: int | None = None
	width: int | None = None
	height: int | None = None
	category: GhnPreviewOrderItemCategory | None = None


class GhnPreviewOrderRequest(BaseModel):
	payment_type_id: int
	note: str | None = None
	required_note: str | None = None
	return_phone: str | None = None
	return_address: str | None = None
	return_district_id: int | None = None
	return_ward_code: str | None = None
	client_order_code: str | None = None
	to_name: str | None = None
	to_phone: str | None = None
	to_address: str | None = None
	to_ward_code: str | None = None
	to_district_id: int | None = None
	cod_amount: int | None = None
	content: str | None = None
	weight: int | None = None
	length: int | None = None
	width: int | None = None
	height: int | None = None
	pick_station_id: int | None = None
	insurance_value: int | None = None
	service_id: int | None = None
	service_type_id: int | None = None
	coupon: str | None = None
	pick_shift: list[int] | None = None
	items: list[GhnPreviewOrderItem] | None = None


__all__ += [
	"GhnA5TokenRequest",
	"GhnCancelOrderRequest",
	"GhnCreateOrderRequest",
	"GhnLeadtimeRequest",
	"GhnOrderDetailRequest",
	"GhnPreviewOrderRequest",
	"GhnReturnOrderRequest",
	"GhnSwitchStatusStoringRequest",
	"GhnUpdateCODRequest",
	"GhnUpdateOrderRequest",
]


class GhnFeeItem(BaseModel):
	name: str
	quantity: int
	height: int
	weight: int
	length: int
	width: int


class GhnFeeRequest(BaseModel):
	from_district_id: int
	from_ward_code: str
	service_id: int
	service_type_id: int | None = None
	to_district_id: int
	to_ward_code: str
	height: int
	length: int
	weight: int
	width: int
	insurance_value: int | None = None
	cod_failed_amount: int | None = None
	coupon: str | None = None
	items: list[GhnFeeItem] | None = None


class GhnAvailableServicesRequest(BaseModel):
	shop_id: int
	from_district: int
	to_district: int


__all__ += [
	"GhnAvailableServicesRequest",
	"GhnFeeItem",
	"GhnFeeRequest",
]
