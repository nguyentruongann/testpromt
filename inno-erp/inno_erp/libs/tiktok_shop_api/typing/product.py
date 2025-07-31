from typing import Literal

from pydantic import BaseModel

from .attribute import TiktokShopAttribute
from .brand import TiktokShopBrand


class TiktokShopListingQuality(BaseModel):
	current_tier: Literal["POOR", "FAIR", "GOOD"] | None = None
	remaining_recommendations: int | None = None


class TiktokShopDiagnosisResult(BaseModel):
	code: str
	how_to_solve: str
	quality_tier: str


class TiktokShopSeoWord(BaseModel):
	text: str


class TiktokShopProductSearchRequest(BaseModel):
	status: Literal[
		"ALL",
		"DRAFT",
		"PENDING",
		"FAILED",
		"ACTIVATE",
		"SELLER_DEACTIVATED",
		"PLATFORM_DEACTIVATED",
		"FREEZE",
		"DELETED",
	] = "ALL"
	seller_skus: list[str] | None = None
	create_time_ge: int | None = None
	create_time_le: int | None = None
	update_time_ge: int | None = None
	update_time_le: int | None = None
	category_version: str | None = None
	listing_quality_tiers: list[Literal["POOR", "FAIR", "GOOD"]] | None = None
	listing_platforms: list[Literal["TOKOPEDIA", "TIKTOK_SHOP"]] | None = None
	audit_status: list[Literal["AUDITING", "FAILED", "APPROVED"]] | None = None
	sku_ids: list[str] | None = None


class TiktokShopAudit(BaseModel):
	status: Literal["NONE", "AUDITING", "FAILED", "PRE_APPROVED", "APPROVED"]
	pre_approved_reasons: list[str] | None = None


class TiktokShopPrice(BaseModel):
	tax_exclusive_price: str | None = None
	sale_price: str | None = None
	amount: str | None = None
	currency: Literal[
		"BRL",
		"EUR",
		"GBP",
		"IDR",
		"JPY",
		"MXN",
		"MYR",
		"PHP",
		"SGD",
		"THB",
		"USD",
		"VND",
	] = "VND"
	unit_price: str | None = None


class TiktokShopImage(BaseModel):
	height: int | None
	width: int | None
	thumb_urls: list[str] | None
	uri: str
	urls: list[str] | None
	locals: list[str] | None = None
	optimization_mode: list[str] | None = None
	original_uri: str | None = None
	original_url: str | None = None
	optimized_uri: str | None = None
	optimized_url: str | None = None
	optimized_status: Literal["SUCCESS", "IGNORE", "PROCESSING"] | None = None


class TiktokShopIdentifierCode(BaseModel):
	type: Literal["EAN", "GTIN", "ISBN", "UPC"]
	value: str


class TiktokShopSalesAttribute(BaseModel):
	id: str | None
	name: str | None
	value_id: str | None
	value_name: str | None
	sku_img: TiktokShopImage | None = None
	supplementary_sku_images: list[TiktokShopImage] | None = None


class TiktokShopCombinedSku(BaseModel):
	product_id: str
	sku_id: str
	sku_count: int


class TiktokShopReplicateSource(BaseModel):
	product_id: str
	shop_id: str
	sku_id: str


class TiktokShopGlobalListingPolicy(BaseModel):
	price_sync: bool
	inventory_type: str
	replicate_source: TiktokShopReplicateSource | None = None


class TiktokShopExternalListPrice(BaseModel):
	source: str
	amount: str
	currency: str


class TiktokShopFulfillmentType(BaseModel):
	handling_duration_days: int
	release_date: int | None = None


class TiktokShopPreSale(BaseModel):
	type: Literal["PRE_SALE", "MADE_TO_ORDER", "CUSTOM"]
	fulfillment_type: TiktokShopFulfillmentType


class TiktokShopListPrice(BaseModel):
	amount: str
	currency: str


class TiktokShopInventory(BaseModel):
	product_id: str | None = None
	skus: list[dict] | None = None
	quantity: int
	warehouse_id: str


class TiktokShopSku(BaseModel):
	id: str | None = None
	seller_sku: str | None = None
	price: TiktokShopPrice
	inventory: list[TiktokShopInventory] | None = None
	identifier_code: TiktokShopIdentifierCode | None = None
	sales_attributes: list[TiktokShopSalesAttribute] | None = None
	external_sku_id: str | None = None
	combined_skus: list[TiktokShopCombinedSku] | None = None
	global_listing_policy: TiktokShopGlobalListingPolicy | None = None
	sku_unit_count: str | None = None
	external_urls: list[str] | None = None
	extra_identifier_codes: list[str] | None = None
	pre_sale: TiktokShopPreSale | None = None
	list_price: TiktokShopListPrice | None = None
	external_list_prices: list[TiktokShopExternalListPrice] | None = None


class TiktokShopCategoryChain(BaseModel):
	id: str
	parent_id: str
	local_name: str
	is_leaf: bool


class TiktokShopVideo(BaseModel):
	id: str
	cover_url: str | None
	format: str | None
	url: str | None
	width: int | None
	height: int | None
	size: int | None


class TiktokShopPackageDimensions(BaseModel):
	length: str
	width: str
	height: str
	unit: str


class TiktokShopPackageWeight(BaseModel):
	value: str
	unit: Literal["KILOGRAM", "POUND", "GRAM"]


class TiktokShopFile(BaseModel):
	id: str
	urls: list[str]
	name: str
	format: str


class TiktokShopCertification(BaseModel):
	id: str
	title: str
	files: list[TiktokShopFile]
	images: list[TiktokShopImage]
	expiration_date: int


class TiktokShopTemplate(BaseModel):
	id: str


class TiktokShopSizeChart(BaseModel):
	images: list[TiktokShopImage]
	template: TiktokShopTemplate


class TiktokShopAuditFailedReason(BaseModel):
	position: str
	reasons: list[str]
	suggestions: list[str]
	listing_platform: str


class TiktokShopDeliveryOption(BaseModel):
	id: str
	name: str
	is_available: bool


class TiktokShopRecommendedCategory(BaseModel):
	id: str
	local_name: str


class TiktokShopIntegratedPlatformStatus(BaseModel):
	platform: str
	status: str


class TiktokShopSalesAttributeMapping(BaseModel):
	local_attribute_id: str
	global_attribute_id: str
	local_value_id: str
	global_value_id: str


class TiktokShopSkuMapping(BaseModel):
	global_sku_id: str
	local_sku_id: str
	sales_attribute_mappings: list[TiktokShopSalesAttributeMapping]


class TiktokShopGlobalProductAssociation(BaseModel):
	global_product_id: str
	sku_mappings: list[TiktokShopSkuMapping]


class TiktokShopPrescriptionRequirement(BaseModel):
	needs_prescription: bool


class TiktokShopSuggestionItem(BaseModel):
	text: str


class TiktokShopSuggestion(BaseModel):
	field: str | None = None
	items: list[TiktokShopSuggestionItem] | None = None


class TiktokShopProduct(BaseModel):
	audit: TiktokShopAudit
	create_time: int
	id: str
	is_not_for_sale: bool
	recommended_categories: list[str]
	sales_regions: list[str]
	skus: list[TiktokShopSku]
	status: str
	title: str
	update_time: int
	listing_quality: TiktokShopListingQuality | None = None
	diagnoses: list[TiktokShopDiagnosisResult] | None = None
	seo_words: list[TiktokShopSeoWord] | None = None
	suggestions: list[TiktokShopSuggestion] | None = None


class TiktokShopSearchProductsResponse(BaseModel):
	next_page_token: str
	products: list[TiktokShopProduct]
	total_count: int


class TiktokShopProductFamily(BaseModel):
	id: str
	products: list[dict]


class TiktokShopGetProductDetailResponse(BaseModel):
	"""
	Response model for the get product detail API.
	"""

	id: str
	status: Literal[
		"DRAFT",
		"PENDING",
		"FAILED",
		"ACTIVATE",
		"SELLER_DEACTIVATED",
		"PLATFORM_DEACTIVATED",
		"FREEZE",
		"DELETED",
	]
	title: str
	category_chains: list[TiktokShopCategoryChain]
	brand: TiktokShopBrand | None = None
	main_images: list[TiktokShopImage]
	video: TiktokShopVideo | None = None
	description: str
	package_dimensions: TiktokShopPackageDimensions
	package_weight: TiktokShopPackageWeight
	skus: list[TiktokShopSku]
	certifications: list[TiktokShopCertification] | None = None
	size_chart: TiktokShopSizeChart | None = None
	is_cod_allowed: bool
	product_attributes: list[TiktokShopAttribute] | None = None
	audit_failed_reasons: list[TiktokShopAuditFailedReason] | None = None
	update_time: int
	create_time: int
	delivery_options: list[TiktokShopDeliveryOption] | None = None
	external_product_id: str | None = None
	product_types: list[Literal["COMBINED_PRODUCT", "IN_COMBINED_PRODUCT", "GPR_TARGET_PRODUCT"]] | None = (
		None
	)
	is_not_for_sale: bool
	recommended_categories: list[TiktokShopRecommendedCategory]
	manufacturer_ids: list[str] | None = None
	responsible_person_ids: list[str] | None = None
	listing_quality_tier: Literal["POOR", "FAIR", "GOOD"] | None = None
	integrated_platform_statuses: list[TiktokShopIntegratedPlatformStatus] | None = None
	shipping_insurance_requirement: Literal["REQUIRED", "OPTIONAL", "NOT_SUPPORTED"] | None = None
	minimum_order_quantity: int | None = None
	is_pre_owned: bool | None = None
	audit: TiktokShopAudit
	global_product_association: TiktokShopGlobalProductAssociation | None = None
	prescription_requirement: TiktokShopPrescriptionRequirement | None = None
	product_families: list[TiktokShopProductFamily] | None = None


class TiktokShopMainImage(BaseModel):
	uri: str


class TiktokShopValue(BaseModel):
	id: str
	name: str


class TiktokShopProductAttribute(BaseModel):
	id: str
	values: list[TiktokShopValue]


class TiktokShopCheckProductListingRequest(BaseModel):
	description: str
	category_id: str
	brand_id: str | None = None
	main_image: list[TiktokShopImage]
	skus: list[TiktokShopSku]
	title: str
	is_cod_allowed: bool | None = None
	certifications: list[TiktokShopCertification] | None
	package_weight: TiktokShopPackageWeight
	product_attributes: list[TiktokShopAttribute] | None = None
	size_chart: TiktokShopSizeChart | None = None
	package_dimensions: TiktokShopPackageDimensions | None = None
	external_product_id: str | None = None
	delivery_option_ids: list[str] | None = None
	video: TiktokShopVideo | None = None
	primary_combined_product_id: str | None = None
	manufacturer_ids: list[str] | None = None
	responsible_person_ids: list[str] | None = None
	listing_platforms: list[str] | None
	shipping_insurance_requirement: str
	is_pre_owned: bool | None = None
	minimum_order_quantity: int | None = None


class TiktokShopFailReason(BaseModel):
	code: str | None = None
	message: str | None = None


class TiktokShopWarning(BaseModel):
	message: str | None = None


class TiktokShopSmartText(BaseModel):
	text: str


class TiktokShopSuggestion(BaseModel):
	seo_words: list[TiktokShopSeoWord]
	smart_texts: list[TiktokShopSmartText]
	images: list[TiktokShopImage]


class TiktokShopDiagnosis(BaseModel):
	field: str
	diagnosis_results: list[TiktokShopDiagnosisResult]
	suggestion: TiktokShopSuggestion


class TiktokShopCheckProductListingResponse(BaseModel):
	check_result: Literal["PASS", "FAILED"]
	fail_reasons: list[TiktokShopFailReason]
	warnings: list[TiktokShopWarning]
	listing_quality: TiktokShopListingQuality
	diagnoses: dict


class TiktokShopUploadProductImageRequest(BaseModel):
	data: bytes
	use_case: str | None = None


class TiktokShopUploadProductImageResponse(BaseModel):
	uri: str
	url: str
	height: int
	width: int
	use_case: str


class TiktokShopUploadProductFileRequest(BaseModel):
	data: str
	name: str


class TiktokShopUploadProductFileResponse(BaseModel):
	id: str
	url: str
	name: str
	format: str


class TiktokShopImageSizeChart(BaseModel):
	uri: str
	urls: list[str]
	height: int
	width: int


class TiktokShopSearchSizeChartsRequest(BaseModel):
	ids: list[str] | None = None
	keyword: str | None = None


class TikSearchSizeChartsResponse(BaseModel):
	size_charts: list[TiktokShopSizeChart]
	total_count: int
	next_page_token: str | None = None


class TiktokShopCreateProductRequest(BaseModel):
	save_mode: str | None = "LISTING"
	description: str
	category_id: str
	brand_id: str | None = None
	main_images: list[TiktokShopMainImage]
	skus: list[TiktokShopSku]
	title: str
	is_cod_allowed: bool | None = None
	certifications: list[TiktokShopCertification] | None = None
	package_weight: TiktokShopPackageWeight
	product_attributes: list[TiktokShopProductAttribute] | None = None
	size_chart: TiktokShopSizeChart | None = None
	package_dimensions: TiktokShopPackageDimensions | None = None
	video: TiktokShopVideo | None = None
	external_product_id: str | None = None
	delivery_option_ids: list[str] | None = None
	primary_combined_product_id: str | None = None
	is_not_for_sale: bool | None = None
	category_version: str | None = None
	manufacturer_ids: list[str] | None = None
	responsible_person_ids: list[str] | None = None
	listing_platforms: list[str] | None = None
	shipping_insurance_requirement: str | None = None
	is_pre_owned: bool | None = None
	minimum_order_quantity: int | None = None
	idempotency_key: str | None = None


class TiktokShopSkuCreateProductResponse(BaseModel):
	id: str
	sales_attributes: list[TiktokShopSalesAttribute]
	seller_sku: str
	price: dict | None = None
	inventory: list[dict] | None = None


class TiktokShopSalesAttributeCreateProductResponse(BaseModel):
	id: str
	value_id: str


# class TiktokShopSkuCreateProductResponse(BaseModel):
# 	id: str
# 	sales_attributes: list[TiktokShopSalesAttributeCreateProductResponse]
# 	seller_sku: str


class TiktokShopCreateProductResponse(BaseModel):
	product_id: str
	skus: list[TiktokShopSkuCreateProductResponse]


class TiktokShopPartialEditProductRequest(BaseModel):
	description: str | None = None
	brand_id: str | None = None
	main_images: list[TiktokShopMainImage] | None = None
	skus: list[dict] | None = None
	title: str | None = None
	is_cod_allowed: bool | None = None
	certifications: list[dict] | None = None
	package_weight: dict | None = None
	product_attributes: list[dict] | None = None
	size_chart: dict | None = None
	package_dimensions: dict | None = None
	video: dict | None = None
	external_product_id: str | None = None
	manufacturer_ids: list[str] | None = None
	responsible_person_ids: list[str] | None = None
	listing_platforms: list[str] | None = None


class TiktokShopPartialEditProductResponse(BaseModel):
	product_id: str
	skus: list[TiktokShopSku]
	audit: TiktokShopAudit


class TiktokShopEditProductRequest(BaseModel):
	description: str
	category_id: str
	brand_id: str | None = None
	main_images: list[TiktokShopMainImage]
	skus: list[TiktokShopSku]
	title: str
	is_cod_allowed: bool | None = None
	package_weight: dict
	certifications: list[TiktokShopCertification] | None = None
	product_attributes: list[TiktokShopProductAttribute] | None = None
	size_chart: TiktokShopSizeChart | None = None
	package_dimensions: TiktokShopPackageDimensions | None = None
	external_product_id: str | None = None
	delivery_option_ids: list[str] | None = None
	video: dict | None = None
	category_version: str | None = None
	manufacturer_ids: list[str] | None = None
	responsible_person_ids: list[str] | None = None
	listing_platforms: list[str] | None = None
	shipping_insurance_requirement: str | None = None
	is_pre_owned: bool | None = None
	minimum_order_quantity: int | None = None


class TiktokShopEditProductResponse(BaseModel):
	product_id: str
	skus: list[TiktokShopSku]
	warnings: list[TiktokShopWarning]
	audit: TiktokShopAudit


class TiktokShopActivateProductRequest(BaseModel):
	product_ids: list[str]
	listing_platforms: list[str] | None = None


class TiktokShopError(BaseModel):
	code: int
	message: str
	detail: dict


class TiktokShopActivateProductResponse(BaseModel):
	errors: list[TiktokShopError]


class TiktokShopDeactivateProductRequest(BaseModel):
	product_ids: list[str]
	listing_platforms: list[str] | None = None


class TiktokShopDeactivateProductResponse(BaseModel):
	errors: list[TiktokShopError]


class TiktokShopDeleteProductRequest(BaseModel):
	product_ids: list[str]


class TiktokShopDeleteProductResponse(BaseModel):
	errors: list[TiktokShopError]


class TiktokShopRecoverProductRequest(BaseModel):
	product_ids: list[str]


class TiktokShopRecoverProductResponse(BaseModel):
	errors: list[TiktokShopError]


class TiktokShopUpdatePriceRequest(BaseModel):
	skus: list[TiktokShopSku]


class TiktokShopUpdatePriceResponse(BaseModel):
	data: dict


class TiktokShopUpdateInventoryRequest(BaseModel):
	skus: list[TiktokShopSku]


class TiktokShopUpdateInventoryResponse(BaseModel):
	errors: list[TiktokShopError]


class TiktokShopInventorySearchRequest(BaseModel):
	product_ids: list[str]
	sku_ids: list[str]


class TiktokShopInventorySearchResponse(BaseModel):
	inventory: TiktokShopInventory


class TiktokShopDiagnoseOptimizeProductRequest(BaseModel):
	product_id: str | None = None
	category_id: str
	description: str | None = None
	brand_id: str | None = None
	main_images: list[TiktokShopMainImage] | None = None
	title: str | None = None
	product_attributes: list[TiktokShopProductAttribute] | None = None
	size_chart: TiktokShopSizeChart | None = None
	optimization_fields: list[str] | None = None


class TiktokShopDiagnoseOptimizeProductResponse(BaseModel):
	listing_quality: TiktokShopListingQuality
	diagnoses: list[TiktokShopDiagnosis]


class TiktokShopProductInformationIssueDiagnosisResponse(BaseModel):
	products: list[TiktokShopProduct]


class TiktokShopGetProductsSeoWordsResponse(BaseModel):
	product: list[TiktokShopProduct]


class TiktokShopGetRecommendedProductTitleAndDescriptionResponse(BaseModel):
	products: list[TiktokShopProduct]


class TiktokShopOptimizedImageRequest(BaseModel):
	images: list[TiktokShopImage]


class TiktokShopCheckListingPrerequisites(BaseModel):
	check_item: str
	is_failed: bool
	failed_reason: list[str]


class TiktokShopCheckResult(BaseModel):
	is_failed: bool
	failed_reason: list[str] | None = None


class TiktokShopCheckItem(BaseModel):
	id: str
	name: str
	check_result: TiktokShopCheckResult


class TiktokShopLogistics(BaseModel):
	delivery_option: str | None = None
	pickup_warehouse: str | None = None
	return_warehouse: str | None = None
	shipping_template: str | None = None


class TiktokShopGne(BaseModel):
	epr: str | None = None
	product_quantity_limit: str | None = None


class TiktokShopShop(BaseModel):
	bank_account: str | None = None
	contact_info: str | None = None
	gne: TiktokShopGne | None = None
	logistics: TiktokShopLogistics | None = None
	status: str | None = None
	tax_info: str | None = None


class TiktokShopCheckListingPrerequisitesResponse(BaseModel):
	shop: TiktokShopShop
