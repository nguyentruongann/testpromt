import json

from .client import LazadaClient
from .typing import (
	LazadaAddReviewReplyRequest,
	LazadaAddReviewReplyResponse,
	LazadaReviewHistoryRequest,
	LazadaReviewHistoryResponse,
	LazadaReviewListRequest,
	LazadaReviewListResponse,
)


class LazadaReview:
	def __init__(self, client: LazadaClient):
		self.client = client

	def get_review_history(self, request: LazadaReviewHistoryRequest) -> LazadaReviewHistoryResponse:
		path = "/review/seller/history/list"
		params = {
			"item_id": str(request.item_id).strip(),
			"start_time": str(request.start_time),
			"end_time": str(request.end_time),
			"current": str(request.current),
		}
		if request.order_id:
			params["order_id"] = str(request.order_id).strip()
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaReviewHistoryResponse(**response)

	def get_review_list_by_id_list(self, request: LazadaReviewListRequest) -> LazadaReviewListResponse:
		path = "/review/seller/list/v2"
		params = {"id_list": json.dumps([str(id).strip() for id in request.id_list])}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaReviewListResponse(**response)

	def add_review_reply(self, request: LazadaAddReviewReplyRequest) -> LazadaAddReviewReplyResponse:
		path = "/review/seller/reply/add"
		params = {"id": str(request.id).strip(), "content": request.content}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaAddReviewReplyResponse(**response)
