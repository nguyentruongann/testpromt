from pydantic import BaseModel

from .base import LazadaResponse


# Voucher product SKU management models
class LazadaSellerVoucherDeleteSelectedProductSKURequest(BaseModel):
	voucher_type: str
	id: int
	sku_ids: list[int]


class LazadaSellerVoucherDeleteSelectedProductSKUResponse(LazadaResponse):
	pass


class LazadaSellerVoucherAddSelectedProductSKURequest(BaseModel):
	voucher_type: str
	id: int
	sku_ids: list[int]


class LazadaSellerVoucherAddSelectedProductSKUResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Voucher activation/deactivation models
class LazadaSellerVoucherActivateRequest(BaseModel):
	voucher_type: str
	id: int


class LazadaSellerVoucherActivateResponse(LazadaResponse):
	pass


class LazadaSellerVoucherDeactivateRequest(BaseModel):
	voucher_type: str
	id: int


class LazadaSellerVoucherDeactivateResponse(LazadaResponse):
	pass


# Voucher creation models
class LazadaSellerVoucherCreateRequest(BaseModel):
	criteria_over_money: str
	voucher_type: str
	apply: str
	collect_start: int | None = None
	display_area: str
	period_end_time: int
	voucher_name: str
	voucher_discount_type: str
	offering_money_value_off: str | None = None
	period_start_time: int
	limit: int
	issued: int
	max_discount_offering_money_value: str | None = None
	offering_percentage_discount_off: float | None = None


class LazadaSellerVoucherCreateResponse(LazadaResponse):
	data: int | None = None


# Voucher update models
class LazadaSellerVoucherUpdateRequest(BaseModel):
	id: str
	criteria_over_money: str
	voucher_type: str
	apply: str
	collect_start: int | None = None
	display_area: str
	period_end_time: int
	voucher_name: str
	voucher_discount_type: str
	offering_money_value_off: str
	period_start_time: int
	limit: int
	issued: int
	max_discount_offering_money_value: str | None = None
	offering_percentage_discount_off: float | None = None


class LazadaSellerVoucherUpdateResponse(LazadaResponse):
	data: int | None = None


# Voucher query models
class LazadaSellerVoucherDetailQueryRequest(BaseModel):
	voucher_type: str
	id: int


class LazadaSellerVoucherDetailQueryResponse(LazadaResponse):
	data: dict[str, any] | None = None


class LazadaSellerVoucherListRequest(BaseModel):
	voucher_type: str
	cur_page: int | None = None
	name: str | None = None
	page_size: int | None = None
	status: str | None = None


class LazadaSellerVoucherListResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Voucher product list models
class LazadaSellerVoucherSelectedProductListRequest(BaseModel):
	voucher_type: str
	id: int
	cur_page: int | None = None
	page_size: int | None = None


class LazadaSellerVoucherSelectedProductListResponse(LazadaResponse):
	data: dict[str, any] | None = None
