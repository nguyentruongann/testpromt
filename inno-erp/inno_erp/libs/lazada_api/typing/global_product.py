from pydantic import BaseModel

from .base import LazadaResponse


# Request models
class LazadaGlobalSku(BaseModel):
	seller_sku: str
	price: float
	quantity: int


class LazadaCreateGlobalProductRequest(BaseModel):
	primary_category_id: int
	attributes: dict[str, any]
	skus: list[LazadaGlobalSku]


class LazadaUnfilledGlobalAttributesRequest(BaseModel):
	page_index: int
	page_size: int
	language_code: str
	attribute_tag: str = "key_prop"


class LazadaAvailableSemiGlobalProductsRequest(BaseModel):
	page_no: int
	page_size: int
	type: str = "semi_global"


class LazadaUpdateSemiGlobalProductRequest(BaseModel):
	item_id: str
	skus: list[dict[str, any]]
	country: str


class LazadaUpgradeSemiGlobalProductRequest(BaseModel):
	item_id: str
	country: str


class LazadaUpdateGlobalProductAttributesRequest(BaseModel):
	item_id: str
	attributes: dict[str, any]


class LazadaDeleteGlobalProductRequest(BaseModel):
	product_id: str
	type: str = "global"


class LazadaUpdateGlobalProductStatusRequest(BaseModel):
	product_id: str
	status: str
	type: str = "global"


# Response models
class LazadaCreateGlobalProductResponse(LazadaResponse):
	pass


class LazadaExtendGlobalProductResponse(LazadaResponse):
	pass


class LazadaGlobalProductStatusResponse(LazadaResponse):
	pass


class LazadaSemiGlobalRecommendedPriceResponse(LazadaResponse):
	pass


class LazadaUnfilledGlobalAttributesResponse(LazadaResponse):
	pass


class LazadaAvailableSemiGlobalProductsResponse(LazadaResponse):
	pass


class LazadaUpdateSemiGlobalProductResponse(LazadaResponse):
	pass


class LazadaUpgradeSemiGlobalProductResponse(LazadaResponse):
	pass


class LazadaUpdateGlobalProductAttributesResponse(LazadaResponse):
	pass


class LazadaDeleteGlobalProductResponse(LazadaResponse):
	pass


class LazadaUpdateGlobalProductStatusResponse(LazadaResponse):
	pass
