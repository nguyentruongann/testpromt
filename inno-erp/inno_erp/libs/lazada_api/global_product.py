import json
import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET

from .client import LazadaClient
from .typing import (
	LazadaAvailableSemiGlobalProductsRequest,
	LazadaAvailableSemiGlobalProductsResponse,
	LazadaCreateGlobalProductRequest,
	LazadaCreateGlobalProductResponse,
	LazadaDeleteGlobalProductRequest,
	LazadaDeleteGlobalProductResponse,
	LazadaExtendGlobalProductResponse,
	LazadaGlobalProductStatusResponse,
	LazadaSemiGlobalRecommendedPriceResponse,
	LazadaUnfilledGlobalAttributesRequest,
	LazadaUnfilledGlobalAttributesResponse,
	LazadaUpdateGlobalProductAttributesRequest,
	LazadaUpdateGlobalProductAttributesResponse,
	LazadaUpdateGlobalProductStatusRequest,
	LazadaUpdateGlobalProductStatusResponse,
	LazadaUpdateSemiGlobalProductRequest,
	LazadaUpdateSemiGlobalProductResponse,
	LazadaUpgradeSemiGlobalProductRequest,
	LazadaUpgradeSemiGlobalProductResponse,
)


class LazadaGlobalProduct:
	def __init__(self, client: LazadaClient):
		self.client = client

	def create_global_product(
		self, request: LazadaCreateGlobalProductRequest
	) -> LazadaCreateGlobalProductResponse:
		path = "/product/global/create"
		# Try different JSON payload format
		payload = {
			"primary_category": request.primary_category_id,
			"attributes": request.attributes,
			"skus": [
				{"seller_sku": sku.seller_sku, "price": sku.price, "quantity": sku.quantity}
				for sku in request.skus
			],
		}
		params = {"payload": json.dumps(payload)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaCreateGlobalProductResponse(**response)

	def extend_global_product(self, item_id: int) -> LazadaExtendGlobalProductResponse:
		path = "/product/global/extension"
		response = self.client.make_request(path, params={item_id}, method="GET")
		return LazadaExtendGlobalProductResponse(**response)

	def get_global_product_status(self, item_id: int) -> LazadaGlobalProductStatusResponse:
		path = "/product/global/status/get"
		response = self.client.make_request(path, params={item_id}, method="GET")
		return LazadaGlobalProductStatusResponse(**response)

	def get_semi_global_recommended_price(self, item_id: int) -> LazadaSemiGlobalRecommendedPriceResponse:
		path = "/product/global/semi/recommend/price/get"
		payload = {"itemId": item_id}
		params = {"payload": json.dumps(payload)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaSemiGlobalRecommendedPriceResponse(**response)

	def get_unfilled_global_attributes(
		self, request: LazadaUnfilledGlobalAttributesRequest
	) -> LazadaUnfilledGlobalAttributesResponse:
		path = "/product/global/unfilled/attribute/get"
		params = {
			"page_index": str(request.page_index),
			"page_size": str(request.page_size),
			"language_code": request.language_code,
			"attribute_tag": request.attribute_tag,
		}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaUnfilledGlobalAttributesResponse(**response)

	def get_available_semi_global_products(
		self, request: LazadaAvailableSemiGlobalProductsRequest
	) -> LazadaAvailableSemiGlobalProductsResponse:
		path = "/product/global/semi/avaible/get"
		params = {
			"pageNo": str(request.page_no),
			"pageSize": str(request.page_size),
			"type": request.type,
			"currentIndex": "0",  # Fixed value
		}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaAvailableSemiGlobalProductsResponse(**response)

	def update_semi_global_product(
		self, request: LazadaUpdateSemiGlobalProductRequest
	) -> LazadaUpdateSemiGlobalProductResponse:
		path = "/product/global/semi/update"
		payload = {
			"itemId": str(request.item_id).strip(),
			"Skus": {"Sku": request.skus},
			"country": request.country,
		}
		params = {"payload": json.dumps(payload)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaUpdateSemiGlobalProductResponse(**response)

	def upgrade_semi_global_product(
		self, request: LazadaUpgradeSemiGlobalProductRequest
	) -> LazadaUpgradeSemiGlobalProductResponse:
		path = "/product/global/semi/upgrade"
		payload = {"item_id": str(request.item_id).strip(), "country": request.country}
		params = {"payload": json.dumps(payload)}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaUpgradeSemiGlobalProductResponse(**response)

	def update_global_product_attributes(
		self, request: LazadaUpdateGlobalProductAttributesRequest
	) -> LazadaUpdateGlobalProductAttributesResponse:
		path = "/product/global/attribute/update"
		request_elem = ET.Element("Request")
		product = ET.SubElement(request_elem, "Product")
		item_id_elem = ET.SubElement(product, "ItemId")
		item_id_elem.text = str(request.item_id).strip()
		attributes_elem = ET.SubElement(product, "Attributes")
		for key, value in request.attributes.items():
			attr = ET.SubElement(attributes_elem, key)
			attr.text = str(value)
		xml_str = (
			minidom.parseString(ET.tostring(request_elem, encoding="unicode"))
			.toprettyxml(indent="  ", encoding="utf-8")
			.decode("utf-8")
		)
		params = {"payload": xml_str}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaUpdateGlobalProductAttributesResponse(**response)

	def delete_global_product(
		self, request: LazadaDeleteGlobalProductRequest
	) -> LazadaDeleteGlobalProductResponse:
		path = "/product/global/delete"
		params = {"productId": str(request.product_id).strip(), "type": request.type}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaDeleteGlobalProductResponse(**response)

	def update_global_product_status(
		self, request: LazadaUpdateGlobalProductStatusRequest
	) -> LazadaUpdateGlobalProductStatusResponse:
		path = "/product/global/update/status"
		params = {
			"productId": str(request.product_id).strip(),
			"status": request.status,
			"type": request.type,
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaUpdateGlobalProductStatusResponse(**response)
