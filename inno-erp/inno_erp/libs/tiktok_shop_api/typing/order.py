from pydantic import BaseModel


class TiktokShopDistrictInfo(BaseModel):
	address_level: str
	address_level_name: str
	address_name: str


class TiktokShopRecipientAddress(BaseModel):
	address_detail: str
	address_line1: str
	address_line2: str
	address_line3: str
	address_line4: str
	district_info: list[TiktokShopDistrictInfo]
	first_name: str
	first_name_local_script: str
	full_address: str
	last_name: str
	last_name_local_script: str
	name: str
	phone_number: str
	postal_code: str
	region_code: str


class TiktokShopPayment(BaseModel):
	currency: str
	original_shipping_fee: str
	original_total_product_price: str
	platform_discount: str
	seller_discount: str
	shipping_fee: str
	shipping_fee_cofunded_discount: str
	shipping_fee_platform_discount: str
	shipping_fee_seller_discount: str
	sub_total: str
	tax: str
	total_amount: str


class TiktokShopLineItem(BaseModel):
	cancel_reason: str
	cancel_user: str
	currency: str
	display_status: str
	id: str
	is_gift: bool
	original_price: str
	package_id: str
	package_status: str
	platform_discount: str
	product_id: str
	product_name: str
	sale_price: str
	seller_discount: str
	seller_sku: str
	shipping_provider_id: str
	shipping_provider_name: str
	sku_id: str
	sku_image: str
	sku_name: str
	sku_type: str
	tracking_number: str


class TiktokShopPackage(BaseModel):
	id: str


class TiktokShopOrder(BaseModel):
	buyer_email: str
	buyer_message: str
	cancel_order_sla_time: int
	cancel_reason: str
	cancel_time: int
	cancellation_initiator: str
	collection_due_time: int
	commerce_platform: str
	create_time: int
	delivery_option_id: str
	delivery_option_name: str
	delivery_type: str
	fulfillment_type: str
	has_updated_recipient_address: bool
	id: str
	is_cod: bool
	is_on_hold_order: bool
	is_replacement_order: bool
	is_sample_order: bool
	line_items: list[TiktokShopLineItem]
	packages: list[TiktokShopPackage]
	paid_time: int
	payment: TiktokShopPayment
	payment_method_name: str
	recipient_address: TiktokShopRecipientAddress
	rts_sla_time: int
	shipping_due_time: int
	shipping_provider: str
	shipping_provider_id: str
	shipping_type: str
	status: str
	tracking_number: str
	tts_sla_time: int
	update_time: int
	user_id: str
	warehouse_id: str


class TiktokShopGetOrderListResponse(BaseModel):
	next_page_token: str
	orders: list[TiktokShopOrder]


class TiktokShopGetOrderDetailsResponse(BaseModel):
	orders: list[TiktokShopOrder]


class TiktokShopLineItemPriceDetail(BaseModel):
	currency: str
	id: str
	net_price_amount: str
	payment: str
	shipping_fee_deduction_platform: str
	shipping_fee_deduction_platform_voucher: str
	shipping_fee_deduction_seller: str
	shipping_list_price: str
	shipping_sale_price: str
	sku_gift_original_price: str
	sku_list_price: str
	sku_sale_price: str
	subtotal: str
	subtotal_deduction_platform: str
	subtotal_deduction_seller: str
	subtotal_tax_amount: str
	tax_amount: str
	total: str
	voucher_deduction_platform: str
	voucher_deduction_seller: str


class TiktokShopGetPriceDetailResponse(BaseModel):
	currency: str
	line_items: list[TiktokShopLineItemPriceDetail]
	net_price_amount: str
	payment: str
	shipping_fee_deduction_platform: str
	shipping_fee_deduction_platform_voucher: str
	shipping_fee_deduction_seller: str
	shipping_list_price: str
	shipping_sale_price: str
	sku_list_price: str
	sku_sale_price: str
	subtotal: str
	subtotal_deduction_platform: str
	subtotal_deduction_seller: str
	subtotal_tax_amount: str
	tax_amount: str
	total: str
	voucher_deduction_platform: str
	voucher_deduction_seller: str
	next_page_token: str | None = None


class TiktokShopSkuCancelRequest(BaseModel):
	sku_id: str
	quantity: int


class TiktokShopCancelOrderRequest(BaseModel):
	order_id: str
	skus: list[TiktokShopSkuCancelRequest] | None = None
	order_line_item_ids: list[str] | None = None
	cancel_reason: str


class TiktokShopCancelOrderResponse(BaseModel):
	cancel_id: str
	cancel_status: str
