from pydantic import BaseModel

from .base import LazadaResponse


# Seller info
# Seller information
class LazadaGetSeller(BaseModel):
	name_company: str | None = None
	logo_url: str | None = None
	name: str | None = None
	short_code: str | None = None
	verified: bool | None = None
	location: str | None = None
	marketplaceEaseMode: bool | None = None
	seller_id: int | None = None
	email: str | None = None
	cb: bool | None = None
	status: str | None = None


class LazadaGetSellerResponse(LazadaResponse):
	data: LazadaGetSeller | None = None


class LazadaSellerMetrics(BaseModel):
	main_category_name: str | None = None
	seller_id: int | None = None
	response_rate: str | None = None
	response_time: str | None = None
	ship_on_time: str | None = None
	main_category_id: int | None = None
	positive_seller_rating: str | None = None


class LazadaGetSellerMetricsResponse(LazadaResponse):
	data: LazadaSellerMetrics | None = None


# class LazadaPickupStore(BaseModel):
# 	headers: dict[str, any] | None = None
# 	success: bool | None = None
# 	model: dict[str, any] | None = None
# 	biz_ext_map: dict[str, any] | None = None
# 	mapping_code: str | None = None
# 	msg_info: str | None = None
# 	msg_code: str | None = None
# 	http_status_code: int | None = None


# class LazadaGetPickupStoreListResponse(LazadaResponse):
# 	result: LazadaPickupStore | None = None


# class LazadaSellerPerformance(BaseModel):
# 	overall_score: float | None = None
# 	order_fulfillment: dict[str, any] | None = None
# 	customer_service: dict[str, any] | None = None
# 	reliability: dict[str, any] | None = None
# 	product_quality: dict[str, any] | None = None


# class LazadaGetSellerPerformanceResponse(LazadaResponse):
# 	data: LazadaSellerPerformance | None = None


# # Voucher management for sellers
# class LazadaCreateVoucherRequest(BaseModel):
# 	title: str
# 	description: str
# 	discount_type: str
# 	discount_value: float
# 	min_spend: float | None = None
# 	start_date: str
# 	end_date: str
# 	usage_limit: int | None = None
# 	usage_limit_per_customer: int | None = None
# 	target_buyer_type: str | None = None
# 	target_products: list[str] | None = None
# 	status: str = "active"


# class LazadaCreateVoucherResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaUpdateVoucherRequest(BaseModel):
# 	voucher_id: str
# 	title: str | None = None
# 	description: str | None = None
# 	status: str | None = None


# class LazadaUpdateVoucherResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaGetVouchersRequest(BaseModel):
# 	status: str | None = None
# 	limit: int = 50
# 	offset: int = 0


# class LazadaVoucher(BaseModel):
# 	voucher_id: str | None = None
# 	title: str | None = None
# 	description: str | None = None
# 	discount_type: str | None = None
# 	discount_value: float | None = None
# 	min_spend: float | None = None
# 	start_date: str | None = None
# 	end_date: str | None = None
# 	usage_limit: int | None = None
# 	usage_limit_per_customer: int | None = None
# 	used_count: int | None = None
# 	status: str | None = None
# 	created_at: str | None = None
# 	updated_at: str | None = None


# class LazadaGetVouchersData(BaseModel):
# 	vouchers: list[LazadaVoucher] | None = None
# 	total_count: int | None = None


# class LazadaGetVouchersResponse(LazadaResponse):
# 	data: LazadaGetVouchersData | None = None


# class LazadaDeleteVoucherRequest(BaseModel):
# 	voucher_id: str


# class LazadaDeleteVoucherResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# # Seller shop management
# class LazadaShopInfo(BaseModel):
# 	shop_id: str | None = None
# 	name: str | None = None
# 	logo: str | None = None
# 	description: str | None = None
# 	location: str | None = None
# 	rating: float | None = None
# 	followers: int | None = None
# 	products_count: int | None = None
# 	created_at: str | None = None
# 	updated_at: str | None = None


# class LazadaGetShopInfoRequest(BaseModel):
# 	pass


# class LazadaGetShopInfoResponse(LazadaResponse):
# 	data: LazadaShopInfo | None = None


# class LazadaUpdateShopInfoRequest(BaseModel):
# 	name: str | None = None
# 	description: str | None = None
# 	logo: str | None = None


# class LazadaUpdateShopInfoResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# # Seller followers
# class LazadaFollower(BaseModel):
# 	buyer_id: str | None = None
# 	name: str | None = None
# 	avatar: str | None = None
# 	followed_at: str | None = None
# 	is_following: bool | None = None


# class LazadaGetFollowersRequest(BaseModel):
# 	limit: int = 50
# 	offset: int = 0


# class LazadaGetFollowersData(BaseModel):
# 	followers: list[LazadaFollower] | None = None
# 	total_count: int | None = None


# class LazadaGetFollowersResponse(LazadaResponse):
# 	data: LazadaGetFollowersData | None = None


# # Seller categories
# class LazadaSellerCategory(BaseModel):
# 	category_id: int | None = None
# 	name: str | None = None
# 	parent_id: int | None = None
# 	level: int | None = None
# 	product_count: int | None = None


# class LazadaGetSellerCategoriesRequest(BaseModel):
# 	pass


# class LazadaGetSellerCategoriesResponse(LazadaResponse):
# 	data: list[LazadaSellerCategory] | None = None


# # Seller store decoration
# class LazadaStoreDecoration(BaseModel):
# 	banner_url: str | None = None
# 	theme_color: str | None = None
# 	description: str | None = None
# 	featured_products: list[str] | None = None


# class LazadaGetStoreDecorationRequest(BaseModel):
# 	pass


# class LazadaGetStoreDecorationResponse(LazadaResponse):
# 	data: LazadaStoreDecoration | None = None


# class LazadaUpdateStoreDecorationRequest(BaseModel):
# 	banner_url: str | None = None
# 	theme_color: str | None = None
# 	description: str | None = None
# 	featured_products: list[str] | None = None


# class LazadaUpdateStoreDecorationResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaBatchQueryShopFollowStatusRequest(BaseModel):
# 	buyer_ids: list[str]


# class LazadaGetSellerShopInfo(BaseModel):
# 	success: bool
# 	error: dict | None = None
# 	result: dict | None = None


# class LazadaBatchQueryShopFollowStatusResponse(LazadaResponse):
# 	result: LazadaGetSellerShopInfo | None = None


# class LazadaGetWarehouseBySellerId(LazadaResponse):
# 	not_success: bool | None = None
# 	success: bool | None = None
# 	module: list[dict[str, any]] | None = None
# 	error_code: str | None = None
# 	repeated: bool | None = None
# 	retry: bool | None = None
# 	class_name: str | None = None


# class LazadaGetWarehouseBySellerIdResponse(LazadaResponse):
# 	result: LazadaGetWarehouseBySellerId | None = None


# class LazadaQueryWarehouseDetailInfo(LazadaResponse):
# 	not_success: bool | None = None
# 	success: bool | None = None
# 	module: dict[str, any] | None = None
# 	error_code: str | None = None
# 	repeated: bool | None = None
# 	retry: bool | None = None
# 	class_name: str | None = None


# class LazadaQueryWarehouseDetailInfoResponse(LazadaResponse):
# 	result: LazadaQueryWarehouseDetailInfo | None = None
