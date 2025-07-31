from pydantic import BaseModel

# Please keep __all__ alphabetized within each category.
__all__ = [
	"Address4LevelRequest",
	"FeeRequest",
	"FeeResponse",
	"GhtkException",
	"GhtkResponse",
	"PickAddResponse",
	"ShopRequest",
	"ShopResponse",
	"ShopToken",
]


class GhtkResponse(BaseModel):
	success: bool
	message: str | None = None


class FeeRequest(BaseModel):
	pick_address_id: str | None = None
	pick_address: str | None = None
	pick_province: str
	pick_district: str
	pick_ward: str | None = None
	pick_street: str | None = None
	address: str | None = None
	province: str
	district: str
	ward: str | None = None
	street: str | None = None
	weight: int
	value: int | None = None
	transport: str | None = None
	deliver_option: str | None = None
	tags: list[int] | None = None


class ExtFee(BaseModel):
	display: str
	title: str
	amount: int
	type: str


class GHTKFee(BaseModel):
	name: str
	fee: int
	insurance_fee: int
	delivery_type: str
	a: int
	dt: str
	extFees: list[ExtFee]
	delivery: bool


class FeeResponse(GhtkResponse):
	fee: GHTKFee


## Order

# https://api.ghtk.vn/docs/submit-order/submit-order-express
GHTK_TAGS = {
	1: "Fragile",  # Dễ vỡ
	2: "High value/Special",  # Giá trị cao/Đặc biệt
	7: "Farm products/Dry food",  # Nông sản/thực phẩm khô
	10: "View product",  # Cho xem hàng
	11: "Try product/Check",  # Cho thử hàng/ đồng kiểm
	13: "Call shop when customer doesn't receive, can't contact, wrong information",  # Gọi shop khi khách không nhận hàng, không liên lạc được, sai thông tin
	17: "Delivery 1 part select product",  # Giao hàng 1 phần chọn sản phẩm
	18: "Delivery 1 part return product",  # Giao hàng 1 phần đổi trả hàng
	19: "Can't deliver and charge",  # Không giao được thu phí
	20: "Box",  # Hàng nguyên hộp
	22: "Letter, document",  # Thư tín, tài liệu
	39: "Fresh food",  # Thực phẩm tươi
	40: "Small",  # Hàng nhỏ
	41: "Don't stack",  # Hàng không xếp chồng
	42: "Stack in the right direction",  # Hàng yêu cầu xếp đúng chiều
	75: "Tree",  # Hàng cây cối
}

GHTK_SUB_TAGS = {
	1: "Seed",  # Hạt giống
	2: "Young tree",  # Cây non
	3: "Tree with fruit",  # Cây có bầu
	4: "Tree with pot",  # Cây có chậu dễ vỡ
	5: "Other tree",  # Các loại cây khác
}


class OrderProduct(BaseModel):
	name: str
	price: int | None = None
	weight: float
	quantity: int | None = None
	product_code: str | None = None


class OrderInfo(BaseModel):
	id: str
	# Pick up
	pick_name: str
	pick_money: int  # 0 if not COD
	pick_address_id: str | None = None
	pick_address: str | None = None
	pick_province: str
	pick_district: str
	pick_ward: str | None = None
	pick_street: str | None = None
	pick_tel: str
	pick_email: str | None = None
	# Delivery
	name: str
	address: str
	province: str
	district: str
	ward: str
	street: str | None = None
	hamlet: str | None = None
	tel: str
	note: str | None = None
	email: str | None = None
	# Return
	use_return_address: bool | None = None
	return_name: str | None = None
	return_address: str | None = None
	return_province: str | None = None
	return_district: str | None = None
	return_ward: str | None = None
	return_street: str | None = None
	return_tel: str | None = None
	return_email: str | None = None
	# Additional
	is_freeship: bool | None = None
	weight_option: str | None = None
	total_weight: float | None = None
	pick_work_shift: int | None = None
	deliver_work_shift: int | None = None
	label_id: str | None = None
	pick_date: str | None = None
	deliver_date: str | None = None
	expired: str | None = None
	value: int
	opm: int | None = None
	pick_option: str | None = None
	actual_transfer_method: str | None = None
	transport: str | None = None
	deliver_option: str | None = None
	tags: list[int] | None = None
	sub_tags: list[int] | None = None


class OrderRequest(BaseModel):
	order: OrderInfo
	products: list[OrderProduct]


class OrderSuccess(BaseModel):
	partner_id: str | None = None
	label: str | None = None
	area: str | None = None
	fee: str | None = None
	insurance_fee: str | None = None
	tracking_id: int | None = None
	estimated_pick_time: str | None = None
	estimated_deliver_time: str | None = None
	products: list[OrderProduct] | None = None
	status_id: int | None = None


class OrderResponse(GhtkResponse):
	order: OrderSuccess


## Tracking Status


class TrackingStatus(BaseModel):
	label_id: str
	partner_id: str
	status: str
	status_text: str
	created: str
	modified: str
	message: str
	pick_date: str | None = None
	deliver_date: str | None = None
	customer_fullname: str | None = None
	customer_tel: str | None = None
	address: str | None = None
	storage_day: int | None = None
	ship_money: int | None = None
	insurance: int | None = None
	value: int | None = None
	weight: int | None = None
	pick_money: int | None = None
	is_freeship: int | None = None


class TrackingStatusResponse(GhtkResponse):
	order: TrackingStatus


## Address4Level
class Address4LevelRequest(BaseModel):
	province: str
	district: str
	ward_street: str
	address: str | None = None


class Address4LevelResponse(GhtkResponse):
	data: list[str] | None = None


## Pick Address
class PickAdd(BaseModel):
	pick_address_id: str | None = None
	address: str | None = None
	pick_tel: str | None = None
	pick_name: str | None = None


class PickAddResponse(GhtkResponse):
	data: list[PickAdd] | None = None


class ShopRequest(BaseModel):
	name: str
	first_address: str
	province: str
	district: str
	tel: str
	email: str


class ShopToken(BaseModel):
	code: str
	token: str


class ShopResponse(BaseModel):
	data: ShopToken


class ShopLoginRequest(BaseModel):
	email: str
	password: str
