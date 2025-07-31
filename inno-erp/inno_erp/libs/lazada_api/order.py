import json

from .client import LazadaClient
from .typing import (
	LazadaGetDocumentRequest,
	LazadaGetDocumentResponse,
	LazadaGetMultipleOrderItemsRequest,
	LazadaGetMultipleOrderItemsResponse,
	LazadaGetOrderItemsRequest,
	LazadaGetOrderItemsResponse,
	LazadaGetOrderRequest,
	LazadaGetOrderResponse,
	LazadaGetOrdersRequest,
	LazadaGetOrdersResponse,
	LazadaGetOVOOrdersRequest,
	LazadaGetOVOOrdersResponse,
	LazadaOrderCancelValidateRequest,
	LazadaOrderCancelValidateResponse,
	LazadaSetInvoiceNumberRequest,
	LazadaSetInvoiceNumberResponse,
)


class LazadaOrder:
	def __init__(self, client: LazadaClient):
		self.client = client

	def get_document(self, request: LazadaGetDocumentRequest) -> LazadaGetDocumentResponse:
		path = "/order/document/get"
		params = {"doc_type": request.doc_type, "order_item_ids": request.order_item_ids}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetDocumentResponse(**response)

	def get_multiple_order_items(
		self, request: LazadaGetMultipleOrderItemsRequest
	) -> LazadaGetMultipleOrderItemsResponse:
		path = "/orders/items/get"
		params = {"order_ids": json.dumps(request.order_ids)}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetMultipleOrderItemsResponse(**response)

	def get_ovo_orders(self, request: LazadaGetOVOOrdersRequest) -> LazadaGetOVOOrdersResponse:
		path = "/orders/ovo/get"
		params = {"tradeOrderIds": request.tradeOrderIds}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetOVOOrdersResponse(**response)

	def get_order(self, order_id: int) -> LazadaGetOrderResponse:
		path = "/order/get"
		response = self.client.make_request(path, params={"order_id": order_id}, method="GET")
		return LazadaGetOrderResponse(**response)

	def get_order_items(self, order_id: int) -> LazadaGetOrderItemsResponse:
		path = "/order/items/get"
		response = self.client.make_request(path, params={"order_id": order_id}, method="GET")
		return LazadaGetOrderItemsResponse(**response)

	def get_orders(self, request: LazadaGetOrdersRequest) -> LazadaGetOrdersResponse:
		path = "/orders/get"
		response = self.client.make_request(path, params=request.model_dump(exclude_none=True), method="GET")
		print(response)
		return LazadaGetOrdersResponse(**response)

	def order_cancel_validate(
		self, request: LazadaOrderCancelValidateRequest
	) -> LazadaOrderCancelValidateResponse:
		path = "/order/reverse/cancel/validate"
		params = {"order_id": request.order_id, "order_item_id_list": json.dumps(request.order_item_id_list)}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaOrderCancelValidateResponse(**response)

	def set_invoice_number(self, request: LazadaSetInvoiceNumberRequest) -> LazadaSetInvoiceNumberResponse:
		path = "/order/invoice_number/set"
		params = {"order_item_id": str(request.order_item_id), "invoice_number": request.invoice_number}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSetInvoiceNumberResponse(**response)
