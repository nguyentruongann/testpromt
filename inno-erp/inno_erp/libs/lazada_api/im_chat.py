from .client import LazadaClient
from .typing import (
	LazadaGetMessagesRequest,
	LazadaGetMessagesResponse,
	LazadaGetSessionDetailRequest,
	LazadaGetSessionDetailResponse,
	LazadaGetSessionListRequest,
	LazadaGetSessionListResponse,
	LazadaMessageRecallRequest,
	LazadaMessageRecallResponse,
	LazadaOpenSessionRequest,
	LazadaOpenSessionResponse,
	LazadaReadSessionRequest,
	LazadaReadSessionResponse,
	LazadaSendMessageRequest,
	LazadaSendMessageResponse,
)


class LazadaInstantMessaging:
	def __init__(self, client: LazadaClient):
		self.client = client

	def get_messages(self, request: LazadaGetMessagesRequest) -> LazadaGetMessagesResponse:
		path = "/im/message/list"
		params = {
			"session_id": request.session_id,
			"start_time": str(request.start_time),
			"page_size": str(request.page_size),
		}
		if request.last_message_id:
			params["last_message_id"] = request.last_message_id
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetMessagesResponse(**response)

	def get_session_detail(self, request: LazadaGetSessionDetailRequest) -> LazadaGetSessionDetailResponse:
		path = "/im/session/get"
		params = {"session_id": request.session_id}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetSessionDetailResponse(**response)

	def get_session_list(self, request: LazadaGetSessionListRequest) -> LazadaGetSessionListResponse:
		path = "/im/session/list"
		params = {"start_time": request.start_time, "page_size": request.page_size}
		if request.last_session_id:
			params["last_session_id"] = request.last_session_id
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetSessionListResponse(**response)

	def message_recall(self, request: LazadaMessageRecallRequest) -> LazadaMessageRecallResponse:
		path = "/im/message/recall"
		params = {"session_id": request.session_id, "message_id": request.message_id}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaMessageRecallResponse(**response)

	def open_session(self, request: LazadaOpenSessionRequest) -> LazadaOpenSessionResponse:
		path = "/im/session/open"
		params = {"order_id": str(request.order_id)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaOpenSessionResponse(**response)

	def read_session(self, request: LazadaReadSessionRequest) -> LazadaReadSessionResponse:
		path = "/im/session/read"
		params = {
			"session_id": request.session_id,
			"last_read_message_id": request.last_read_message_id,
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaReadSessionResponse(**response)

	def send_message(self, request: LazadaSendMessageRequest) -> LazadaSendMessageResponse:
		path = "/im/message/send"
		params = {"session_id": request.session_id, "template_id": request.template_id}
		if request.txt:
			params["txt"] = request.txt
		if request.img_url:
			params["img_url"] = request.img_url
		if request.width is not None:
			params["width"] = str(request.width)
		if request.height is not None:
			params["height"] = str(request.height)
		if request.item_id:
			params["item_id"] = request.item_id
		if request.order_id:
			params["order_id"] = request.order_id
		if request.promotion_id:
			params["promotion_id"] = request.promotion_id
		if request.video_id:
			params["video_id"] = request.video_id
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSendMessageResponse(**response)
