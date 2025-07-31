from pydantic import BaseModel

from .base import TiktokShopResponse


class TiktokShopAuth(BaseModel):
	access_token: str
	access_token_expire_in: int
	refresh_token: str
	refresh_token_expire_in: int
	open_id: str
	seller_name: str
	seller_base_region: str
	user_type: int
	granted_scopes: list[str]
	cipher: str | None = None


class TiktokShopAuthResponse(TiktokShopResponse):
	data: TiktokShopAuth
