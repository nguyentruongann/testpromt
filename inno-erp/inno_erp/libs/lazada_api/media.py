import json

from .client import LazadaClient
from .typing import (
	LazadaCompleteCreateVideoRequest,
	LazadaCompleteCreateVideoResponse,
	LazadaGetVideoQuotaRequest,
	LazadaGetVideoQuotaResponse,
	LazadaGetVideoRequest,
	LazadaGetVideoResponse,
	LazadaInitCreateVideoRequest,
	LazadaInitCreateVideoResponse,
	LazadaRemoveVideoRequest,
	LazadaRemoveVideoResponse,
	LazadaUploadVideoPartRequest,
	LazadaUploadVideoPartResponse,
)


class LazadaMedia:
	def __init__(self, client: LazadaClient):
		self.client = client

	def init_create_video(self, request: LazadaInitCreateVideoRequest) -> LazadaInitCreateVideoResponse:
		path = "/media/video/block/create"
		params = {"fileName": request.fileName, "fileBytes": str(request.fileBytes)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaInitCreateVideoResponse(**response)

	def upload_video_part(self, request: LazadaUploadVideoPartRequest) -> LazadaUploadVideoPartResponse:
		path = "/media/video/block/upload"
		part_size = 5 * 1024 * 1024
		block_count = (len(request.file_part) + part_size - 1) // part_size
		params = {
			"uploadId": request.upload_id,
			"partNumber": str(request.part_number),
			"blockCount": str(block_count),
			"blockNo": str(request.part_number - 1),
		}
		files = {"file": ("part", request.file_part)}
		response = self.client.make_request(path, params=params, method="POST", files=files)
		return LazadaUploadVideoPartResponse(**response)

	def complete_create_video(
		self, request: LazadaCompleteCreateVideoRequest
	) -> LazadaCompleteCreateVideoResponse:
		path = "/media/video/block/commit"
		params = {
			"uploadId": str(request.upload_id).strip(),
			"parts": json.dumps([part.dict() for part in request.parts]),
			"title": request.title,
			"coverUrl": request.cover_url,
		}
		if request.video_usage:
			params["videoUsage"] = request.video_usage
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaCompleteCreateVideoResponse(**response)

	def get_video(self, request: LazadaGetVideoRequest) -> LazadaGetVideoResponse:
		path = "/media/video/get"
		params = {"videoId": str(request.video_id).strip()}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetVideoResponse(**response)

	def get_video_quota(self, request: LazadaGetVideoQuotaRequest) -> LazadaGetVideoQuotaResponse:
		path = "/media/video/quota/get"
		params = {}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetVideoQuotaResponse(**response)

	def remove_video(self, request: LazadaRemoveVideoRequest) -> LazadaRemoveVideoResponse:
		path = "/media/video/remove"
		params = {"videoId": str(request.video_id)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaRemoveVideoResponse(**response)
