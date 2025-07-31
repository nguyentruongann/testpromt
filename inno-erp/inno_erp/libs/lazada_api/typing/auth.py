from pydantic import BaseModel


class LazadaAuthResponse(BaseModel):
	access_token: str
	expires_in: int
	refresh_token: str
	open_id: str | None = None
	seller_name: str | None = None
	seller_base_region: str | None = None
	user_type: int | None = None
	granted_scopes: list[str] | None = None
