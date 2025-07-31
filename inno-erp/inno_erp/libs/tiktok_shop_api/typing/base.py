from pydantic import BaseModel


class TiktokShopResponse(BaseModel):
	code: int
	message: str
	request_id: str
