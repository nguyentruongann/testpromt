from pydantic import BaseModel

from .base import LazadaResponse


# Review history models
class LazadaReviewHistoryRequest(BaseModel):
	item_id: str
	start_time: int
	end_time: int
	current: int
	order_id: str | None = None


class LazadaReviewHistoryResponse(LazadaResponse):
	pass


# Review list models
class LazadaReviewListRequest(BaseModel):
	id_list: list[str]


class LazadaReviewListResponse(LazadaResponse):
	pass


# Review reply models
class LazadaAddReviewReplyRequest(BaseModel):
	id: str
	content: str


class LazadaAddReviewReplyResponse(LazadaResponse):
	pass
