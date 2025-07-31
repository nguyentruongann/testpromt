from .client import LazadaClient
from .typing import (
	LazadaStoreCustomPageRequest,
	LazadaStoreCustomPageResponse,
)


class LazadaStore:
	def __init__(self, client: LazadaClient):
		self.client = client

	def get_store_custom_page(self, request: LazadaStoreCustomPageRequest) -> LazadaStoreCustomPageResponse:
		path = "/store/custom/page/get"
		params = {"page": str(request.page), "size": str(request.size)}
		if request.keyword:
			params["keyword"] = request.keyword
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaStoreCustomPageResponse(**response)
