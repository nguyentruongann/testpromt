from pydantic import BaseModel

from .base import LazadaResponse


# Store custom page models
class LazadaStoreCustomPageRequest(BaseModel):
	page: int
	size: int
	keyword: str | None = None


class LazadaStoreCustomPageResponse(LazadaResponse):
	pass
