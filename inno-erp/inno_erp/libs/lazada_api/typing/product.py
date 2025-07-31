from typing import Any

from pydantic import BaseModel, field_validator
from pydantic_xml import BaseXmlModel, element

from .base import LazadaResponse


class LazadaBrand(BaseModel):
	global_identifier: str | None = None
	name_en: str | None = None
	brand_id: int | None = None
	name: str | None = None


class LazadaGetBrandsByPages(BaseModel):
	start_row: int | None = None
	page_index: int | None = None
	total_page: int | None = None
	module: list[LazadaBrand] | None = None
	enable_total: bool | None = None
	page_size: int | None = None
	total_record: int | None = None
	success: bool | None = None
	error_code: str | None = None
	error_msg: str | None = None


class LazadaGetBrandsByPagesResponse(LazadaResponse):
	data: LazadaGetBrandsByPages | None = None


class LazadaCategorySuggestion(BaseModel):
	categoryId: int | None = None
	categoryName: str | None = None
	categoryPath: str | None = None


class LazadaGetCategorySuggestions(BaseModel):
	categorySuggestions: list[LazadaCategorySuggestion] | None = None


class LazadaGetCategorySuggestionResponse(LazadaResponse):
	data: LazadaGetCategorySuggestions | None = None


class LazadaGetCategorySuggestionInBulk(BaseModel):
	categorySuggestionMap: dict[str, list[LazadaCategorySuggestion]] | None = None


class LazadaGetCategorySuggestionInBulkResponse(LazadaResponse):
	data: LazadaGetCategorySuggestionInBulk | None = None


class LazadaCategoryAttributeOption(BaseModel):
	name: str | None = None
	en_name: str | None = None
	id: int | None = None


class LazadaCategoryAttribute(BaseModel):
	advanced: dict[str, Any] | None = None
	label: str | None = None
	name: str | None = None
	is_mandatory: int | None = None
	attribute_type: str | None = None
	input_type: str | None = None
	options: list[LazadaCategoryAttributeOption] | None = None
	is_sale_prop: int | None = None
	id: int | None = None


class LazadaGetCategoryAttributesResponse(LazadaResponse):
	data: list[LazadaCategoryAttribute] | None = None


class LazadaCategory(BaseModel):
	category_id: int | None = None
	name: str | None = None
	var: bool | None = None
	leaf: bool | None = None
	children: list["LazadaCategory"] | None = None


class LazadaGetCategoryTreeResponse(LazadaResponse):
	data: list[LazadaCategory] | None = None


# class LazadaCascadePropValue(BaseModel):
# 	id: int | None = None
# 	name: str | None = None
# 	leaf: str | None = None


# class LazadaCascadeProp(BaseModel):
# 	id: int | None = None
# 	name: str | None = None
# 	required: bool | None = None
# 	propValue: list[LazadaCascadePropValue] | None = None


# class LazadaGetNextCascadePropData(BaseModel):
# 	prop: LazadaCascadeProp | None = None


# class LazadaGetNextCascadePropResponse(LazadaResponse):
# 	data: LazadaGetNextCascadePropData | None = None


# # Core product models
# class LazadaWarehouseInventory(BaseXmlModel, tag="MultiWarehouseInventory"):
# 	WarehouseCode: str = element()
# 	SellableQuantity: int = element(default=None)
# 	Quantity: int = element(default=None)


# class LazadaMultiWarehouseInventory(BaseXmlModel, tag="MultiWarehouseInventories"):
# 	MultiWarehouseInventory: list[LazadaWarehouseInventory] = element(default=None)


# class LazadaSkuStock(BaseXmlModel, tag="Sku"):
# 	ItemId: int = element()
# 	SkuId: int = element()
# 	SellerSku: str | None = element(default=None)
# 	Quantity: int | None = element(default=None)
# 	SellableQuantity: int | None = element(default=None)
# 	MultiWarehouseInventories: LazadaMultiWarehouseInventory | None = element(default=None)
# 	Price: float | None = element(default=None)
# 	SalePrice: float | None = element(default=None)
# 	SaleStartDate: str | None = element(default=None)
# 	SaleEndDate: str | None = element(default=None)


# class LazadaSkuCreate(BaseModel):
# 	sku_id: str | None = None
# 	seller_sku: str
# 	quantity: int | None = None
# 	price: float | None = None
# 	special_price: float | None = None
# 	special_from_date: str | None = None
# 	special_to_date: str | None = None
# 	package_height: float | None = None
# 	package_length: float | None = None
# 	package_width: float | None = None
# 	package_weight: float | None = None
# 	package_content: str | None = None
# 	coming_soon: str | None = None
# 	delay_delivery_days: int | None = None
# 	images: list[str] | None = None
# 	color_family: str | None = None
# 	size: str | None = None

# 	@field_validator("sku_id", mode="before")
# 	def convert_sku_id_to_str(cls, v):
# 		return str(v) if v is not None else None

# 	@field_validator("quantity", mode="before")
# 	def convert_quantity_to_int(cls, v):
# 		return int(v)

# 	@field_validator(
# 		"price",
# 		"special_price",
# 		"package_height",
# 		"package_length",
# 		"package_width",
# 		"package_weight",
# 		mode="before",
# 	)
# 	def convert_to_float(cls, v):
# 		return float(v) if v is not None else None

# 	@field_validator("delay_delivery_days", mode="before")
# 	def convert_days_to_int(cls, v):
# 		return int(v) if v is not None else None


# class LazadaSkuInfo(BaseModel):
# 	seller_sku: str | None = None
# 	shop_sku: str | None = None
# 	sku_id: str | None = None

# 	@field_validator("sku_id", mode="before")
# 	def convert_sku_id_to_str(cls, v):
# 		return str(v) if v is not None else None


# class LazadaSkuResult(BaseModel):
# 	item_id: str | None = None
# 	sku_id: str | None = None
# 	seller_sku: str | None = None
# 	status: str | None = None
# 	error_code: str | None = None
# 	error_message: str | None = None


# class LazadaSkuDeactivate(BaseModel):
# 	sku_id: str
# 	seller_sku: str

# 	@field_validator("sku_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# # Product creation and management
# class LazadaCreateProductRequest(BaseModel):
# 	primary_category: str
# 	images: list[str]
# 	attributes: dict[str, any]
# 	skus: list[LazadaSkuCreate]

# 	@field_validator("primary_category", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# class LazadaCreateProductData(BaseModel):
# 	item_id: str | None = None
# 	sku_list: list[LazadaSkuInfo] | None = None

# 	@field_validator("item_id", mode="before")
# 	def convert_item_id_to_str(cls, v):
# 		return str(v) if v is not None else None


# class LazadaCreateProductResponse(LazadaResponse):
# 	data: LazadaCreateProductData | None = None


# class LazadaVariation(BaseModel):
# 	name: str | None = None
# 	has_image: bool | None = None
# 	customize: bool | None = None
# 	options: list[str] | None = None


# class LazadaUpdateProductData(BaseModel):
# 	variation: dict[str, LazadaVariation] | None = None


# class LazadaUpdateProductRequest(BaseModel):
# 	item_id: str
# 	attributes: dict[str, any] | None = None
# 	skus: list[LazadaSkuCreate] | None = None
# 	trial_product: bool = False


# class LazadaUpdateProductResponse(LazadaResponse):
# 	data: LazadaUpdateProductData | None = None


# class LazadaDeactivateProductRequest(BaseModel):
# 	item_id: str
# 	skus: list[LazadaSkuDeactivate] | None = None

# 	@field_validator("item_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# class LazadaDeactivateProductResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaRemoveProductRequest(BaseModel):
# 	seller_sku_list: list[str] | None = None
# 	sku_id_list: list[str] | None = None


# class LazadaRemoveProductResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaRemoveSkuRequest(BaseModel):
# 	item_id: str
# 	variation_name: str
# 	sku_ids: list[str]

# 	@field_validator("item_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# class LazadaRemoveSkuResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# # Product validation and checking
# class LazadaProductCheckRequest(BaseModel):
# 	primary_category: str
# 	images: list[str]
# 	attributes: dict[str, any]
# 	skus: list[LazadaSkuCreate]
# 	spu_id: str | None = None
# 	associated_sku: str | None = None

# 	@field_validator("primary_category", "spu_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v) if v is not None else None


# class LazadaProductCheckResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# # Product retrieval


# class LazadaGetProductItem(BaseModel):
# 	created_time: str | None = None
# 	updated_time: str | None = None
# 	images: list[str] | None = None
# 	skus: list[dict[str, any]] | None = None
# 	imageSequence: dict[str, any] | None = None
# 	item_id: int | None = None
# 	hiddenStatus: str | None = None
# 	bizSupplement: dict[str, any] | None = None
# 	subStatus: str | None = None
# 	suspendedSkus: list[dict[str, any]] | None = None
# 	trialProduct: bool | None = None
# 	rejectReason: list[dict[str, any]] | None = None
# 	hiddenReason: str | None = None
# 	variation: dict[str, any] | None = None
# 	primary_category: int | None = None
# 	marketImages: list[str] | None = None
# 	attributes: dict[str, any] | None = None
# 	status: str | None = None


# class LazadaGetProductItemResponse(LazadaResponse):
# 	data: LazadaGetProductItem | None = None


# class LazadaGetProductsRequest(BaseModel):
# 	filter: str | None = None
# 	update_before: str | None = None
# 	create_before: str | None = None
# 	offset: int | None = None
# 	create_after: str | None = None
# 	update_after: str | None = None
# 	limit: int | None = 50
# 	options: int | None = None
# 	sku_seller_list: list[str] | None = None


# class LazadaGetProduct(BaseModel):
# 	item_id: int | None = None
# 	primary_category: int | None = None
# 	attributes: dict[str, any] | None = None
# 	skus: list[dict[str, any]] | None = None
# 	created_time: str | None = None
# 	updated_time: str | None = None
# 	images: list[str] | None = None
# 	marketImages: list[str] | None = None
# 	status: str | None = None
# 	subStatus: str | None = None
# 	suspendedSkus: list[dict[str, any]] | None = None
# 	trialProduct: bool | None = None
# 	rejectReason: list[dict[str, any]] | None = None
# 	hiddenReason: str | None = None
# 	hiddenStatus: str | None = None


# class LazadaGetProducts(BaseModel):
# 	total_products: int | None = None
# 	products: list[LazadaGetProduct] | None = None


# class LazadaGetProductsResponse(LazadaResponse):
# 	data: LazadaGetProducts | None = None


# # Product quality and content
# class LazadaProductContentScore(BaseModel):
# 	score: float | None = None
# 	details: dict[str, any] | None = None


# class LazadaGetProductContentScoreResponse(LazadaResponse):
# 	data: LazadaProductContentScore | None = None


# class LazadaQcAlertProduct(BaseModel):
# 	item_id: int | None = None
# 	alert_reason: str | None = None


# class LazadaGetQcAlertProductsRequest(BaseModel):
# 	offset: int
# 	limit: int


# class LazadaGetQcAlertProductsResponse(LazadaResponse):
# 	data: list[LazadaQcAlertProduct] | None = None


# # Product attributes
# class LazadaAttributeOption(BaseModel):
# 	name: str | None = None


# class LazadaUnfilledAttribute(BaseModel):
# 	advanced: dict[str, any] | None = None
# 	name: str | None = None
# 	input_type: str | None = None
# 	options: list[LazadaAttributeOption] | None = None
# 	is_mandatory: int | None = None
# 	attribute_type: str | None = None
# 	label: str | None = None


# class LazadaUnfilledAttributeItem(BaseModel):
# 	item_id: int | None = None
# 	primary_category: int | None = None
# 	attributes: list[LazadaUnfilledAttribute] | None = None
# 	seller_sku_id: str | None = None
# 	error_msg: str | None = None


# class LazadaGetUnfilledAttributeItemData(BaseModel):
# 	total_products: int | None = None
# 	products: list[LazadaUnfilledAttributeItem] | None = None


# class LazadaGetUnfilledAttributeItemRequest(BaseModel):
# 	page_index: int
# 	page_size: int
# 	language_code: str
# 	attribute_tag: str = "key_prop"


# class LazadaGetUnfilledAttributeItemResponse(LazadaResponse):
# 	success: bool | None = None
# 	data: LazadaGetUnfilledAttributeItemData | None = None


# # Stock management


# class LazadaAdjustSellableStockData(BaseModel):
# 	success: bool | None = None
# 	sku_results: list[LazadaSkuResult] | None = None


# class LazadaAdjustSellableStockResponse(LazadaResponse):
# 	data: LazadaAdjustSellableStockData | None = None


# class LazadaUpdatePriceQuantityResponse(LazadaResponse):
# 	data: LazadaAdjustSellableStockData | None = None


# class LazadaUpdateSellableQuantityResponse(LazadaResponse):
# 	data: LazadaAdjustSellableStockData | None = None


# # Image management
# class LazadaSetImagesRequest(BaseModel):
# 	sku_id: str
# 	image_urls: list[str]

# 	@field_validator("sku_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# class LazadaSetImagesResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaUploadImageData(BaseModel):
# 	image: dict[str, str] | None = None


# class LazadaUploadImageRequest(BaseModel):
# 	image_path: str


# class LazadaUploadImageResponse(LazadaResponse):
# 	data: LazadaUploadImageData | None = None


# class LazadaMigrateImageData(BaseModel):
# 	image: dict[str, str] | None = None


# class LazadaMigrateImageRequest(BaseModel):
# 	image_url: str


# class LazadaMigrateImageResponse(LazadaResponse):
# 	data: LazadaMigrateImageData | None = None


# class LazadaMigrateImagesData(BaseModel):
# 	batch_id: str | None = None


# class LazadaMigrateImagesRequest(BaseModel):
# 	image_urls: list[str]


# class LazadaMigrateImagesResponse(LazadaResponse):
# 	data: LazadaMigrateImagesData | None = None


# class LazadaImageResponse(BaseModel):
# 	batch_id: str | None = None
# 	status: str | None = None
# 	images: list[dict[str, any]] | None = None


# class LazadaGetImageResponseRequest(BaseModel):
# 	batch_id: str


# class LazadaGetImageResponseResponse(LazadaResponse):
# 	data: LazadaImageResponse | None = None


# # Size chart management
# class LazadaSizeChart(BaseModel):
# 	product_id: str
# 	size_chart: str

# 	@field_validator("product_id", mode="before")
# 	def convert_to_str(cls, v):
# 		return str(v)


# class LazadaBatchUpdateSizeChartRequest(BaseModel):
# 	size_charts: list[LazadaSizeChart]


# class LazadaBatchUpdateSizeChartResponse(LazadaResponse):
# 	data: dict[str, any] | None = None


# class LazadaSizeChartTemplate(BaseModel):
# 	template_id: int | None = None
# 	template_name: str | None = None
# 	content: dict[str, any] | None = None


# class LazadaGetSizeChartTemplateRequest(BaseModel):
# 	page_no: int
# 	page_size: int
# 	template_id: int | None = None
# 	template_name: str | None = None

# 	@field_validator("template_id", mode="before")
# 	def convert_to_int(cls, v):
# 		return int(v) if v is not None else None


# class LazadaGetSizeChartTemplateResponse(LazadaResponse):
# 	data: list[LazadaSizeChartTemplate] | None = None


# class LazadaGetPreQcRulesRequest(BaseModel):
# 	option: int
# 	option_set: list[int]


# class LazadaGetPreQcRulesData(BaseModel):
# 	restricted_cate_ids: list[int]
# 	item_limit: int
# 	iitem_counttem_limit: int


# class LazadaGetPreQcRulesResponse(LazadaResponse):
# 	values: LazadaGetPreQcRulesData
