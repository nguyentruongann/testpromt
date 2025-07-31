from pydantic import BaseModel

from .auth import ViettelPostResponse


class InventoryItem(BaseModel):
	groupaddressId: int
	cusId: int
	name: str
	phone: str
	address: str
	provinceId: int
	districtId: int
	wardsId: int
	postId: int | None = None
	merchant: str | None = None


class InventoryResponse(ViettelPostResponse):
	data: list[InventoryItem] | None = None
