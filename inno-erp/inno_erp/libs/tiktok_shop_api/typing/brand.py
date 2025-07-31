from pydantic import BaseModel


class TiktokShopBrand(BaseModel):
	id: str
	name: str
	authorized_status: str | None = None
	brand_status: str | None = None
	is_t1_brand: bool | None = None


class TiktokShopGetBrandsResponse(BaseModel):
	id: str


class TiktokShopCreateBrandRequest(BaseModel):
	name: str


class TiktokShopCreateBrandResponse(BaseModel):
	id: str
