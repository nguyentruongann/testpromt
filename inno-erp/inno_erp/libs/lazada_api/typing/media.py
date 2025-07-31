from pydantic import BaseModel, Field

from .base import LazadaResponse


# Video part models
class LazadaVideoPart(BaseModel):
	partNumber: int
	eTag: str


# Video creation models
class LazadaInitCreateVideoRequest(BaseModel):
	fileName: str
	fileBytes: int


class LazadaInitCreateVideoResponse(LazadaResponse):
	upload_id: str | None = None
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None


# Video upload models
class LazadaUploadVideoPartRequest(BaseModel):
	upload_id: str
	part_number: int
	file_part: bytes


class LazadaUploadVideoPartResponse(LazadaResponse):
	eTag: str | None = Field(None, alias="e_tag")
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None


# Video completion models
class LazadaCompleteCreateVideoRequest(BaseModel):
	upload_id: str
	parts: list[LazadaVideoPart]
	title: str
	cover_url: str
	video_usage: str | None = None


class LazadaCompleteCreateVideoResponse(LazadaResponse):
	video_id: str | None = None
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None


# Video retrieval models
class LazadaGetVideoRequest(BaseModel):
	video_id: str


class LazadaGetVideoResponse(LazadaResponse):
	cover_url: str | None = None
	video_url: str | None = None
	state: str | None = None
	title: str | None = None
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None


# Video quota models
class LazadaGetVideoQuotaRequest(BaseModel):
	pass


class LazadaGetVideoQuotaResponse(LazadaResponse):
	capacity_size: int | None = None
	used_size: int | None = None
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None


# Video removal models
class LazadaRemoveVideoRequest(BaseModel):
	video_id: str


class LazadaRemoveVideoResponse(LazadaResponse):
	success: bool | None = None
	result_code: str | None = None
	result_message: str | None = None
