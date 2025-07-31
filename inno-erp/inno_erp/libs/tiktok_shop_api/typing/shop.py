from pydantic import BaseModel


class TiktokShopAuthorizedShop(BaseModel):
	"""Represents an authorized shop."""

	cipher: str
	code: str
	id: str
	name: str
	region: str
	seller_type: str


class TiktokShopAuthorizedShopResponse(BaseModel):
	"""Data model for GetAuthorizedShop API response."""

	shops: list[TiktokShopAuthorizedShop]


class TiktokShopActiveShop(BaseModel):
	id: str
	region: str


class TiktokShopActiveShopResponse(BaseModel):
	"""Data model for GetAuthorizedShop API response."""

	shops: list[TiktokShopActiveShop]
