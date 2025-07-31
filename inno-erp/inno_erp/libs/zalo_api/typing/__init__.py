from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

__all__ = [
	"ZaloAttachment",
	"ZaloAttachmentElement",
	"ZaloAttachmentPayload",
	"ZaloException",
	"ZaloFilePayload",
	"ZaloHookAttachment",
	"ZaloHookMessage",
	"ZaloListUser",
	"ZaloListUsers",
	"ZaloListUsersRequest",
	"ZaloListUsersResponse",
	"ZaloMessage",
	"ZaloMetadata",
	"ZaloResponse",
	"ZaloSendMessageResponse",
	"ZaloUserDetail",
	"ZaloWebhook",
]


### Common
class ZaloResponse(BaseModel):
	error: int
	message: str


class ZaloException(Exception):
	def __init__(self, message, status_code):
		self.message = message
		self.status_code = status_code


class ZaloAccessTokenResponse(BaseModel):
	access_token: str
	refresh_token: str
	expires_in: str


ZaloResponseType = ZaloResponse | ZaloAccessTokenResponse


class ZaloMetadata(BaseModel):
	code_verifier: str | None = None
	oa_id: str | None = None


### Attachment
class ZaloAttachmentElement(BaseModel):
	media_type: Literal["image", "sticker"]
	url: str | None = None
	attachment_id: str | None = None


class ZaloAttachmentPayload(BaseModel):
	template_type: Literal["media", "request_user_info"]
	elements: list[ZaloAttachmentElement]


class ZaloFilePayload(BaseModel):
	token: str | None = None


class ZaloAttachment(BaseModel):
	type: Literal["template", "file"]
	payload: ZaloAttachmentPayload | ZaloFilePayload


### Message
class ZaloMessage(BaseModel):
	text: str | None = None
	attachment: ZaloAttachment | None = None
	quote_message_id: str | None = None


class ZaloSendMessage(BaseModel):
	quota: dict | None = None
	message_id: str
	user_id: str


class ZaloSendMessageResponse(ZaloResponse):
	data: ZaloSendMessage


### User Detail
class ZaloUserDetail(BaseModel):
	user_id: str
	user_id_by_app: str
	user_external_id: str
	display_name: str
	user_alias: str
	is_sensitive: bool
	user_last_interaction_date: str
	user_is_follower: bool
	avatar: str
	avatars: dict
	tags_and_notes_info: dict[str, list[Any]]
	shared_info: dict


class ZaloUserDetailResponse(ZaloResponse):
	data: ZaloUserDetail


### Webhook
class ZaloHookAttachment(BaseModel):
	type: Literal["image", "gif", "sticker", "link"]
	payload: dict[str, str]


class ZaloHookMessage(BaseModel):
	msg_id: str
	text: str | None = None
	quote_msg_id: str | None = None
	attachments: list[ZaloHookAttachment] | None = None


class ZaloWebhook(BaseModel):
	app_id: str
	sender: dict[str, str]
	user_id_by_app: str | None = None
	recipient: dict[str, str]
	event_name: str
	message: ZaloHookMessage
	timestamp: str


### List Users
class ZaloListUsersRequest(BaseModel):
	offset: int = 0
	count: int = 50
	tag_name: str | None = None
	last_interaction_period: str | None = None
	is_follower: bool | None = None


class ZaloListUser(BaseModel):
	user_id: str


class ZaloListUsers(BaseModel):
	users: list[ZaloListUser]
	total: int
	count: int
	offset: int


class ZaloListUsersResponse(ZaloResponse):
	data: ZaloListUsers
