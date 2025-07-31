from pydantic import BaseModel

from .base import LazadaResponse


# Document models
class LazadaGetDocumentRequest(BaseModel):
	doc_type: str
	order_item_ids: str


class LazadaDocument(BaseModel):
	file: str | None = None
	mime_type: str | None = None
	document_type: str | None = None


class LazadaGetDocumentResponse(LazadaResponse):
	data: dict[str, LazadaDocument] | None = None


# Multiple order items models
class LazadaGetMultipleOrderItemsRequest(BaseModel):
	order_ids: list[int]


class LazadaPickUpStoreInfo(BaseModel):
	pick_up_store_name: str | None = None
	pick_up_store_address: str | None = None
	pick_up_store_code: str | None = None
	pick_up_store_open_hour: list[str] | None = None


class LazadaOrderItem(BaseModel):
	voucher_code_platform: str | None = None
	delivery_option_sof: int | None = None
	is_fbl: int | None = None
	is_reroute: int | None = None
	voucher_seller_lpi: float | None = None
	voucher_platform_lpi: float | None = None
	buyer_id: int | None = None
	pick_up_store_info: LazadaPickUpStoreInfo | None = None
	sku_id: str | None = None
	fulfillment_sla: str | None = None
	priority_fulfillment_tag: str | None = None
	gift_wrapping: str | None = None
	show_gift_wrapping_tag: bool | None = None
	personalization: str | None = None
	show_personalization_tag: bool | None = None
	payment_time: str | None = None
	supply_price: float | None = None
	supply_price_currency: str | None = None
	mp3_order: bool | None = None
	semi_managed: bool | None = None
	biz_group: int | None = None
	schedule_delivery_start_timeslot: int | None = None
	schedule_delivery_end_timeslot: int | None = None
	reason: str | None = None
	digital_delivery_info: str | None = None
	promised_shipping_time: str | None = None
	order_id: int | None = None
	voucher_amount: float | None = None
	return_status: str | None = None
	shipping_type: str | None = None
	shipment_provider: str | None = None
	cancel_return_initiator: str | None = None
	variation: str | None = None
	created_at: str | None = None
	invoice_number: str | None = None
	shipping_amount: float | None = None
	currency: str | None = None
	shop_id: str | None = None
	sku: str | None = None
	voucher_code: str | None = None
	wallet_credits: float | None = None
	updated_at: str | None = None
	is_digital: int | None = None
	tracking_code_pre: str | None = None
	order_item_id: int | None = None
	package_id: str | None = None
	tracking_code: str | None = None
	shipping_service_cost: float | None = None
	extra_attributes: str | None = None
	paid_price: float | None = None
	shipping_provider_type: str | None = None
	product_detail_url: str | None = None
	shop_sku: str | None = None
	reason_detail: str | None = None
	purchase_order_id: str | None = None
	purchase_order_number: str | None = None
	name: str | None = None
	product_main_image: str | None = None
	item_price: float | None = None
	tax_amount: float | None = None
	status: str | None = None
	voucher_platform: float | None = None
	voucher_seller: float | None = None
	order_type: str | None = None
	stage_pay_status: str | None = None
	order_flag: str | None = None
	sla_time_stamp: str | None = None
	warehouse_code: str | None = None
	shipping_fee_original: float | None = None
	shipping_fee_discount_seller: float | None = None
	shipping_fee_discount_platform: float | None = None
	voucher_code_seller: str | None = None


class LazadaMultipleOrderItem(BaseModel):
	order_number: int | None = None
	order_id: int | None = None
	order_items: list[LazadaOrderItem] | None = None


class LazadaGetMultipleOrderItemsResponse(LazadaResponse):
	data: list[LazadaMultipleOrderItem] | None = None


# OVO orders models
class LazadaGetOVOOrdersRequest(BaseModel):
	tradeOrderIds: str


class LazadaTradeOrderLine(BaseModel):
	tradeOrderLineId: int | None = None
	deliveryStatus: str | None = None
	reverseStatus: str | None = None
	deliveredTime: str | None = None


class LazadaTradeOrder(BaseModel):
	tradeOrderId: int | None = None
	paymentMethod: str | None = None
	paidTime: str | None = None
	tradeOrderLines: list[LazadaTradeOrderLine] | None = None


class LazadaGetOVOOrdersResponse(LazadaResponse):
	result: dict[str, any] | None = None


# Single order models
class LazadaGetOrderRequest(BaseModel):
	order_id: int


class LazadaAddress(BaseModel):
	address1: str | None = None
	address2: str | None = None
	address3: str | None = None
	address4: str | None = None
	address5: str | None = None
	addressDistrict: str | None = None
	city: str | None = None
	country: str | None = None
	first_name: str | None = None
	last_name: str | None = None
	phone: str | None = None
	phone2: str | None = None
	post_code: str | None = None


class LazadaOrder(BaseModel):
	address_billing: LazadaAddress | None = None
	address_shipping: LazadaAddress | None = None
	branch_number: str | None = None
	tax_code: str | None = None
	extra_attributes: str | None = None
	shipping_fee: float | None = None
	customer_first_name: str | None = None
	customer_last_name: str | None = None
	payment_method: str | None = None
	statuses: list[str] | None = None
	remarks: str | None = None
	order_number: int | None = None
	order_id: int | None = None
	voucher: float | None = None
	national_registration_number: str | None = None
	promised_shipping_times: str | None = None
	items_count: int | None = None
	created_at: str | None = None
	price: str | None = None
	gift_option: bool | None = None
	delivery_info: str | None = None
	gift_message: str | None = None
	voucher_code: str | None = None
	updated_at: str | None = None
	address_updated_at: str | None = None
	warehouse_code: str | None = None
	shipping_fee_original: float | None = None
	shipping_fee_discount_seller: float | None = None
	shipping_fee_discount_platform: float | None = None
	buyer_note: str | None = None


class LazadaGetOrderResponse(LazadaResponse):
	data: LazadaOrder | None = None


# Order items models
class LazadaGetOrderItemsRequest(BaseModel):
	order_id: int


class LazadaGetOrderItemsResponse(LazadaResponse):
	data: list[LazadaOrderItem] | None = None


# Orders list models
class LazadaGetOrdersRequest(BaseModel):
	sort_by: str | None = None
	created_before: str | None = None
	created_after: str | None = None
	status: str | None = None
	update_before: str | None = None
	sort_direction: str | None = None
	offset: int | None = None
	limit: int | None = None
	update_after: str | None = None


class LazadaGetOrdersResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Order cancel validation models
class LazadaOrderCancelValidateRequest(BaseModel):
	order_id: str
	order_item_id_list: list[str]


class LazadaReasonOption(BaseModel):
	reason_name: str | None = None
	reason_id: str | None = None


class LazadaOrderCancelValidateData(BaseModel):
	tip_content: str | None = None
	tip_type: str | None = None
	reason_options: list[LazadaReasonOption] | None = None


class LazadaOrderCancelValidateResponse(LazadaResponse):
	data: LazadaOrderCancelValidateData | None = None


# Invoice number models
class LazadaSetInvoiceNumberRequest(BaseModel):
	order_item_id: int
	invoice_number: str


class LazadaSetInvoiceNumberData(BaseModel):
	order_item_id: int | None = None
	invoice_number: str | None = None


class LazadaSetInvoiceNumberResponse(LazadaResponse):
	data: LazadaSetInvoiceNumberData | None = None
