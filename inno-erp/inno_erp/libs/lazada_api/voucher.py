import json

from .client import LazadaClient
from .typing import (
	LazadaSellerVoucherActivateRequest,
	LazadaSellerVoucherActivateResponse,
	LazadaSellerVoucherAddSelectedProductSKURequest,
	LazadaSellerVoucherAddSelectedProductSKUResponse,
	LazadaSellerVoucherCreateRequest,
	LazadaSellerVoucherCreateResponse,
	LazadaSellerVoucherDeactivateRequest,
	LazadaSellerVoucherDeactivateResponse,
	LazadaSellerVoucherDeleteSelectedProductSKURequest,
	LazadaSellerVoucherDeleteSelectedProductSKUResponse,
	LazadaSellerVoucherDetailQueryRequest,
	LazadaSellerVoucherDetailQueryResponse,
	LazadaSellerVoucherListRequest,
	LazadaSellerVoucherListResponse,
	LazadaSellerVoucherSelectedProductListRequest,
	LazadaSellerVoucherSelectedProductListResponse,
	LazadaSellerVoucherUpdateRequest,
	LazadaSellerVoucherUpdateResponse,
)


class LazadaSellerVoucher:
	def __init__(self, client: LazadaClient):
		self.client = client

	def delete_selected_product_sku(
		self, request: LazadaSellerVoucherDeleteSelectedProductSKURequest
	) -> LazadaSellerVoucherDeleteSelectedProductSKUResponse:
		path = "/promotion/voucher/product/sku/remove"
		params = {
			"voucher_type": request.voucher_type,
			"id": str(request.id),
			"sku_ids": json.dumps(request.sku_ids),
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherDeleteSelectedProductSKUResponse(**response)

	def activate(self, request: LazadaSellerVoucherActivateRequest) -> LazadaSellerVoucherActivateResponse:
		path = "/promotion/voucher/activate"
		params = {"voucher_type": request.voucher_type, "id": str(request.id)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherActivateResponse(**response)

	def add_selected_product_sku(
		self, request: LazadaSellerVoucherAddSelectedProductSKURequest
	) -> LazadaSellerVoucherAddSelectedProductSKUResponse:
		path = "/promotion/voucher/product/sku/add"
		params = {
			"voucher_type": request.voucher_type,
			"id": str(request.id),
			"sku_ids": json.dumps(request.sku_ids),
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherAddSelectedProductSKUResponse(**response)

	def create(self, request: LazadaSellerVoucherCreateRequest) -> LazadaSellerVoucherCreateResponse:
		path = "/promotion/voucher/create"
		params = {
			"criteria_over_money": request.criteria_over_money,
			"voucher_type": request.voucher_type,
			"apply": request.apply,
			"display_area": request.display_area,
			"period_end_time": str(request.period_end_time),
			"voucher_name": request.voucher_name,
			"voucher_discount_type": request.voucher_discount_type,
			"period_start_time": str(request.period_start_time),
			"limit": str(request.limit),
			"issued": str(request.issued),
		}
		if request.collect_start is not None:
			params["collect_start"] = str(request.collect_start)
		if request.offering_money_value_off:
			params["offering_money_value_off"] = request.offering_money_value_off
		if request.max_discount_offering_money_value:
			params["max_discount_offering_money_value"] = request.max_discount_offering_money_value
		if request.offering_percentage_discount_off is not None:
			params["offering_percentage_discount_off"] = str(request.offering_percentage_discount_off)
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherCreateResponse(**response)

	def deactivate(
		self, request: LazadaSellerVoucherDeactivateRequest
	) -> LazadaSellerVoucherDeactivateResponse:
		path = "/promotion/voucher/deactivate"
		params = {"voucher_type": request.voucher_type, "id": str(request.id)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherDeactivateResponse(**response)

	def detail_query(
		self, request: LazadaSellerVoucherDetailQueryRequest
	) -> LazadaSellerVoucherDetailQueryResponse:
		path = "/promotion/voucher/get"
		params = {"voucher_type": request.voucher_type, "id": str(request.id)}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaSellerVoucherDetailQueryResponse(**response)

	def list(self, request: LazadaSellerVoucherListRequest) -> LazadaSellerVoucherListResponse:
		path = "/promotion/vouchers/get"
		params = {"voucher_type": request.voucher_type}
		if request.cur_page is not None:
			params["cur_page"] = str(request.cur_page)
		if request.name:
			params["name"] = request.name
		if request.page_size is not None:
			params["page_size"] = str(request.page_size)
		if request.status:
			params["status"] = request.status
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaSellerVoucherListResponse(**response)

	def selected_product_list(
		self, request: LazadaSellerVoucherSelectedProductListRequest
	) -> LazadaSellerVoucherSelectedProductListResponse:
		path = "/promotion/voucher/products/get"
		params = {"voucher_type": request.voucher_type, "id": str(request.id)}
		if request.cur_page is not None:
			params["cur_page"] = str(request.cur_page)
		if request.page_size is not None:
			params["page_size"] = str(request.page_size)
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaSellerVoucherSelectedProductListResponse(**response)

	def update(self, request: LazadaSellerVoucherUpdateRequest) -> LazadaSellerVoucherUpdateResponse:
		path = "/promotion/voucher/update"
		params = {
			"id": request.id,
			"criteria_over_money": request.criteria_over_money,
			"voucher_type": request.voucher_type,
			"apply": request.apply,
			"display_area": request.display_area,
			"period_end_time": str(request.period_end_time),
			"voucher_name": request.voucher_name,
			"voucher_discount_type": request.voucher_discount_type,
			"offering_money_value_off": request.offering_money_value_off,
			"period_start_time": str(request.period_start_time),
			"limit": str(request.limit),
			"issued": str(request.issued),
		}
		if request.collect_start is not None:
			params["collect_start"] = str(request.collect_start)
		if request.max_discount_offering_money_value:
			params["max_discount_offering_money_value"] = request.max_discount_offering_money_value
		if request.offering_percentage_discount_off is not None:
			params["offering_percentage_discount_off"] = str(request.offering_percentage_discount_off)
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSellerVoucherUpdateResponse(**response)
