from pydantic import BaseModel


class TiktokShopGeolocation(BaseModel):
	latitude: str
	longitude: str


class TiktokShopDimensionLimit(BaseModel):
	max_height: int
	max_length: int
	max_width: int
	unit: str


class TiktokShopAddress(BaseModel):
	address_line1: str
	city: str
	contact_person: str
	distict: str
	full_address: str
	phone_number: str
	postal_code: str
	region: str
	region_code: str
	state: str
	town: str


class TiktokShopWarehouse(BaseModel):
	address: TiktokShopAddress
	effect_status: str
	id: str
	is_default: bool
	name: str
	sub_type: str
	type: str


class TiktokShopGetWarehouseListResponse(BaseModel):
	warehouses: list[TiktokShopWarehouse]


class TiktokShopWeightLimit(BaseModel):
	max_weight: int
	min_weight: int
	unit: str


class TiktokShopDeliveryOption(BaseModel):
	id: str
	name: str
	type: str
	description: str
	dimension_limit: TiktokShopDimensionLimit
	weight_limit: TiktokShopWeightLimit
	platform: list[str]


class TiktokShopGetDeliveryOptionsResponse(BaseModel):
	delivery_options: list[TiktokShopDeliveryOption]


class TiktokShopShippingProvider(BaseModel):
	id: str
	name: str


class TiktokShopGetShippingProvidersResponse(BaseModel):
	shipping_providers: list[TiktokShopShippingProvider]
