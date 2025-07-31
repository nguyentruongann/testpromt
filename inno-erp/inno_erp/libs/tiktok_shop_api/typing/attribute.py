from pydantic import BaseModel


class TiktokShopAttributeValue(BaseModel):
	id: str
	name: str


class TiktokShopAttribute(BaseModel):
	id: str
	is_customizable: bool | None = None
	is_multiple_selection: bool | None = None
	is_required: bool | None = None
	name: str | None = None
	type: str | None = None
	values: list[TiktokShopAttributeValue] | None = None
	requirement_conditions: list[dict] | None = None
	value_data_format: str | None = None


class TiktokShopGetAttributesResponse(BaseModel):
	attributes: list[TiktokShopAttribute]


class TiktokShopGetGolbalAttributesResponse(BaseModel):
	attributes: list[TiktokShopAttribute]
