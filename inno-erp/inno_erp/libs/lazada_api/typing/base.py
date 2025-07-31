from pydantic import BaseModel, Field


class LazadaResponse(BaseModel):
	"""Base response model for all Lazada API responses."""

	code: str | None = None
	data: dict | None = None
	request_id: str | None = None
	# type: str | None = None
	# message: str | None = None
	trace_id: str | None = Field(None, alias="_trace_id_")
	# success: bool | None = None
	# error: str | None = None
	# errorCode: str | None = None
	# error_msg: str | None = None
	# headers: dict[str, Any] | None = None
	# biz_ext_map: dict[str, Any] | None = None
	# mapping_code: str | None = None
	# msg_info: str | None = None
	# msg_code: str | None = None
	# http_status_code: int | None = None
	# not_success: bool | None = None
	# retry: bool | None = None
	# repeated: bool | None = None
	# class_name: str | None = None
