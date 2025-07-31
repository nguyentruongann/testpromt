from typing import Literal

from pydantic import BaseModel


class TiktokShopCategory(BaseModel):
	id: str
	is_leaf: bool
	local_name: str
	parent_id: str
	permission_statuses: list[str]


class TiktokShopManufacturer(BaseModel):
	is_required: bool | None = None
	optional_regions: dict | None
	required_regions: dict | None


class TiktokShopResponsiblePerson(BaseModel):
	is_required: bool | None = None
	optional_regions: dict
	required_regions: dict


class TiktokShopRequirementCondition(BaseModel):
	region: (
		Literal["DE", "ES", "FR", "GB", "ID", "IT", "IE", "JP", "MY", "PH", "SG", "TH", "US", "VN"] | None
	) = None
	condition_type: str | None = None
	attribute_id: str | None = None
	attribute_value_id: str | None = None


class TiktokShopGetCategoriesResponse(BaseModel):
	categories: list[TiktokShopCategory]


class TiktokShopCategoryRuleItem(BaseModel):
	is_required: bool | None = None
	is_supported: bool | None = None


class TiktokShopCategoryRulesResponse(BaseModel):
	cod: dict
	epr: dict
	manufacturer: dict
	package_dimension: dict
	product_certifications: list[dict]
	responsible_person: dict
	size_chart: dict
	allowed_special_product_types: dict | None = None


class TiktokShopImage(BaseModel):
	uri: str


class TiktokShopImages(BaseModel):
	images: list[TiktokShopImage]


class TiktokShopRecommendCategoryRequest(BaseModel):
	product_title: str
	description: str | None = None
	images: TiktokShopImages | None = None
	category_version: str | None = None
	listing_platform: str | None = None
	include_prohibited_categories: bool | None = None


class TiktokShopRecommendedCategory(BaseModel):
	leaf_category_id: str
	category_id: TiktokShopCategory


class TiktokShopRecommendedCategoriesResponse(BaseModel):
	recommended_categories: list[TiktokShopRecommendedCategory]
