from pydantic import BaseModel

from .base import LazadaResponse


# Message models
class LazadaMessage(BaseModel):
	from_account_type: int | None = None
	to_account_type: int | None = None
	from_account_id: str | None = None
	message_id: str | None = None
	to_account_id: str | None = None
	site_id: str | None = None
	session_id: str | None = None
	template_id: int | None = None
	type: int | None = None
	content: str | None = None
	send_time: int | None = None
	process_msg: str | None = None
	status: int | None = None
	auto_reply: bool | None = None


# Get messages models
class LazadaGetMessagesRequest(BaseModel):
	session_id: str
	start_time: int
	page_size: int
	last_message_id: str | None = None


class LazadaGetMessagesResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Session detail models
class LazadaGetSessionDetailRequest(BaseModel):
	session_id: str


class LazadaGetSessionDetailResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Session list models
class LazadaGetSessionListRequest(BaseModel):
	start_time: str
	page_size: str
	last_session_id: str | None = None


class LazadaGetSessionListResponse(LazadaResponse):
	data: dict[str, any] | None = None


# Message recall models
class LazadaMessageRecallRequest(BaseModel):
	session_id: str
	message_id: str


class LazadaMessageRecallResponse(LazadaResponse):
	pass


# Open session models
class LazadaOpenSessionRequest(BaseModel):
	order_id: int


class LazadaOpenSessionResponse(BaseModel):
	session_id: str | None = None


# Read session models
class LazadaReadSessionRequest(BaseModel):
	session_id: str
	last_read_message_id: str


class LazadaReadSessionResponse(LazadaResponse):
	pass


# Send message models
class LazadaSendMessageRequest(BaseModel):
	session_id: str
	template_id: str
	txt: str | None = None
	img_url: str | None = None
	width: int | None = None
	height: int | None = None
	item_id: str | None = None
	order_id: str | None = None
	promotion_id: str | None = None
	video_id: str | None = None


class LazadaSendMessageResponse(LazadaResponse):
	data: dict[str, any] | None = None
