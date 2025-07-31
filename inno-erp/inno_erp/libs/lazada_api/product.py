import json

from .client import LazadaClient
from .typing import *


class LazadaProductAPI:
	def __init__(self, client: LazadaClient):
		self.client = client

	# def adjust_sellable_stock(self, skus: list[LazadaSkuStock]) -> LazadaAdjustSellableStockResponse:
	# 	path = "/product/stock/sellable/adjust"
	# 	payload = "".join([sku.to_xml(exclude_none=True).decode("utf-8") for sku in skus])
	# 	params = {"payload": f"<Request><Product><Skus>{payload}</Skus></Product></Request>"}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaAdjustSellableStockResponse(**response)

	# def batch_update_size_chart(
	# 	self, request: LazadaBatchUpdateSizeChartRequest
	# ) -> LazadaBatchUpdateSizeChartResponse:
	# 	path = "/size/chart/batch/update"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"SizeCharts": {
	# 					"SizeChart": [
	# 						{
	# 							"product_id": str(chart.product_id),
	# 							"size_chart": chart.size_chart,
	# 						}
	# 						for chart in request.size_charts
	# 					]
	# 				}
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaBatchUpdateSizeChartResponse(**response)

	# def create_product(self, request: LazadaCreateProductRequest) -> LazadaCreateProductResponse:
	# 	path = "/product/create"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"PrimaryCategory": str(request.primary_category),
	# 				"Images": {"Image": request.images},
	# 				"Attributes": request.attributes,
	# 				"Skus": {
	# 					"Sku": [
	# 						{
	# 							"SellerSku": sku.seller_sku,
	# 							"quantity": str(sku.quantity),
	# 							"price": str(sku.price),
	# 							"color_family": sku.color_family,
	# 							"size": sku.size,
	# 							"package_length": str(sku.package_length) if sku.package_length else None,
	# 							"package_height": str(sku.package_height) if sku.package_height else None,
	# 							"package_weight": str(sku.package_weight) if sku.package_weight else None,
	# 							"package_width": str(sku.package_width) if sku.package_width else None,
	# 							"package_content": sku.package_content,
	# 							"Images": {"Image": sku.images} if sku.images else None,
	# 						}
	# 						for sku in request.skus
	# 					]
	# 				},
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaCreateProductResponse(**response)

	# def deactivate_product(self, request: LazadaDeactivateProductRequest) -> LazadaDeactivateProductResponse:
	# 	path = "/product/deactivate"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"ItemId": str(request.item_id),
	# 				"Skus": [{"SkuId": str(sku.sku_id), "SellerSku": sku.seller_sku} for sku in request.skus]
	# 				if request.skus
	# 				else None,
	# 			}
	# 		}
	# 	}
	# 	params = {"apiRequestBody": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaDeactivateProductResponse(**response)

	def get_brands_by_pages(self, start_row: int = 0, page_size: int = 20) -> LazadaGetBrandsByPagesResponse:
		path = "/category/brands/query"
		params = {"startRow": start_row, "pageSize": page_size}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetBrandsByPagesResponse(**response)

	def get_category_attributes(
		self, primary_category_id: str, language_code: str = "vi_VN"
	) -> LazadaGetCategoryAttributesResponse:
		path = "/category/attributes/get"
		response = self.client.make_request(
			path,
			params={
				"primary_category_id": primary_category_id,
				"language_code": language_code,
			},
			method="GET",
		)
		return LazadaGetCategoryAttributesResponse(**response)

	def get_category_suggestion(self, product_name: str) -> LazadaGetCategorySuggestionResponse:
		path = "/product/category/suggestion/get"
		response = self.client.make_request(path, params={"product_name": product_name}, method="GET")
		return LazadaGetCategorySuggestionResponse(**response)

	def get_category_suggestion_in_bulk(
		self, product_name_list: list[str]
	) -> LazadaGetCategorySuggestionInBulkResponse:
		path = "/product/category/suggestion/get/batch"
		params = {"product_name_list": json.dumps(product_name_list)}
		response = self.client.make_request(path, params=params, method="GET")
		return LazadaGetCategorySuggestionInBulkResponse(**response)

	def get_category_tree(self, language_code: str = "vi_VN") -> LazadaGetCategoryTreeResponse:
		path = "/category/tree/get"
		response = self.client.make_request(
			path, params={"language_code": language_code}, method="GET", required_auth=False
		)
		return LazadaGetCategoryTreeResponse(**response)

	# def get_next_cascade_prop(
	# 	self, categoryId: int, cascadeId: int, path: str | None = None
	# ) -> LazadaGetNextCascadePropResponse:
	# 	path = "/category/cascade/getNextCascadeProp"
	# 	params = {"categoryId": categoryId, "cascadeId": cascadeId}
	# 	if path:
	# 		params["path"] = path
	# 	response = self.client.make_request(path, params=params, method="GET")
	# 	return LazadaGetNextCascadePropResponse(**response)

	# def get_pre_qc_rules(self, request: LazadaGetPreQcRulesRequest) -> LazadaGetPreQcRulesResponse:
	# 	path = "/product/seller/item/getPreQcRules"
	# 	params = {"option": str(request.option), "option_set": json.dumps(request.option_set)}
	# 	response = self.client.call_api(path, params=params, method="GET")
	# 	return LazadaGetPreQcRulesResponse(**response)

	# def get_product_content_score(self, item_id: int) -> LazadaGetProductContentScoreResponse:
	# 	path = "/product/content/score/get"
	# 	response = self.client.make_request(path, params={item_id: item_id}, method="GET")
	# 	return LazadaGetProductContentScoreResponse(**response)

	# def get_product_item(self, item_id: int, seller_sku: str | None = None) -> LazadaGetProductItemResponse:
	# 	path = "/product/item/get"

	# 	params = {"item_id": item_id}
	# 	if seller_sku:
	# 		params["seller_sku"] = seller_sku

	# 	response = self.client.make_request(path, params=params, method="GET")
	# 	return LazadaGetProductItemResponse(**response)

	# def get_products(self, request: LazadaGetProductsRequest) -> LazadaGetProductsResponse:
	# 	path = "/products/get"
	# 	response = self.client.make_request(path, params=request.model_dump(exclude_none=True), method="GET")
	# 	return LazadaGetProductsResponse(**response)

	# def get_qc_alert_products(
	# 	self, request: LazadaGetQcAlertProductsRequest
	# ) -> LazadaGetQcAlertProductsResponse:
	# 	path = "/product/qc/alert/list"
	# 	response = self.client.make_request(path, params=request.model_dump(exclude_none=True), method="GET")
	# 	return LazadaGetQcAlertProductsResponse(**response)

	# def get_image_response(self, request: LazadaGetImageResponseRequest) -> LazadaGetImageResponseResponse:
	# 	path = "/image/response/get"
	# 	params = {"batch_id": request.batch_id}
	# 	response = self.client.make_request(path, params=params, method="GET")
	# 	return LazadaGetImageResponseResponse(**response)

	# def get_seller_item_limit(
	# 	self, request: LazadaGetSellerItemLimitRequest
	# ) -> LazadaGetSellerItemLimitResponse:
	# 	path = "/product/seller/item/limit"
	# 	response = self.client.call_api(path, params={}, method="GET")
	# 	return LazadaGetSellerItemLimitResponse(**response)

	# def get_size_chart_template(
	# 	self, request: LazadaGetSizeChartTemplateRequest
	# ) -> LazadaGetSizeChartTemplateResponse:
	# 	path = "/size/chart/template/get"
	# 	params = {"page_no": str(request.page_no), "page_size": str(request.page_size)}
	# 	if request.template_id is not None:
	# 		params["template_id"] = str(request.template_id)
	# 	if request.template_name:
	# 		params["template_name"] = request.template_name
	# 	response = self.client.make_request(path, params=params, method="GET")
	# 	return LazadaGetSizeChartTemplateResponse(**response)

	# def get_unfilled_attribute_item(
	# 	self, request: LazadaGetUnfilledAttributeItemRequest
	# ) -> LazadaGetUnfilledAttributeItemResponse:
	# 	path = "/product/unfilled/attribute/get"
	# 	params = {
	# 		"page_index": str(request.page_index),
	# 		"attribute_tag": request.attribute_tag,
	# 		"page_size": str(request.page_size),
	# 		"language_code": request.language_code,
	# 	}
	# 	response = self.client.make_request(path, params=params, method="GET")
	# 	parsed_response = LazadaGetUnfilledAttributeItemResponse(**response)
	# 	return parsed_response

	# def migrate_image(self, request: LazadaMigrateImageRequest) -> LazadaMigrateImageResponse:
	# 	path = "/image/migrate"
	# 	payload = {"Request": {"Image": {"Url": request.image_url}}}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaMigrateImageResponse(**response)

	# def migrate_images(self, request: LazadaMigrateImagesRequest) -> LazadaMigrateImagesResponse:
	# 	path = "/images/migrate"
	# 	payload = {"Request": {"Images": [{"Url": url} for url in request.image_urls]}}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaMigrateImagesResponse(**response)

	# def product_check(self, request: LazadaProductCheckRequest) -> LazadaProductCheckResponse:
	# 	path = "/product/pre/check"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"PrimaryCategory": str(request.primary_category),
	# 				"SPUId": request.spu_id if request.spu_id else "",
	# 				"AssociatedSku": request.associated_sku if request.associated_sku else "",
	# 				"Images": {"Image": request.images},
	# 				"Attributes": request.attributes,
	# 				"Skus": [
	# 					{
	# 						"SellerSku": sku.seller_sku,
	# 						"quantity": str(sku.quantity),
	# 						"price": str(sku.price),
	# 						"color_family": sku.color_family,
	# 						"size": sku.size,
	# 						"package_length": str(sku.package_length) if sku.package_length else None,
	# 						"package_height": str(sku.package_height) if sku.package_height else None,
	# 						"package_weight": str(sku.package_weight) if sku.package_weight else None,
	# 						"package_width": str(sku.package_width) if sku.package_width else None,
	# 						"package_content": sku.package_content,
	# 						"Images": {"Image": sku.images} if sku.images else None,
	# 					}
	# 					for sku in request.skus
	# 				],
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaProductCheckResponse(**response)

	# def remove_product(self, request: LazadaRemoveProductRequest) -> LazadaRemoveProductResponse:
	# 	path = "/product/remove"
	# 	params = {
	# 		"seller_sku_list": json.dumps(request.seller_sku_list) if request.seller_sku_list else None,
	# 		"sku_id_list": json.dumps(request.sku_id_list) if request.sku_id_list else None,
	# 	}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaRemoveProductResponse(**response)

	# def remove_sku(self, request: LazadaRemoveSkuRequest) -> LazadaRemoveSkuResponse:
	# 	path = "/product/sku/remove"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"ItemId": str(request.item_id),
	# 				"Variation": {"Variation1": {"name": request.variation_name}},
	# 				"Skus": [{"SkuId": str(sku_id)} for sku_id in request.sku_ids],
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaRemoveSkuResponse(**response)

	# def set_images(self, request: LazadaSetImagesRequest) -> LazadaSetImagesResponse:
	# 	path = "/images/set"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"Skus": [
	# 					{
	# 						"SkuId": str(request.sku_id),
	# 						"Images": {"Image": request.image_urls},
	# 					}
	# 				]
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaSetImagesResponse(**response)

	# def update_price_quantity(self, skus: list[LazadaSkuStock]) -> LazadaUpdatePriceQuantityResponse:
	# 	path = "/product/price_quantity/update"
	# 	# Fix: Properly decode bytes to string instead of using str() which includes b''
	# 	payload = "".join([sku.to_xml(exclude_none=True).decode("utf-8") for sku in skus])
	# 	params = {"payload": f"<Request><Product><Skus>{payload}</Skus></Product></Request>"}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaUpdatePriceQuantityResponse(**response)

	# def update_product(self, request: LazadaUpdateProductRequest) -> LazadaUpdateProductResponse:
	# 	path = "/product/update"
	# 	payload = {
	# 		"Request": {
	# 			"Product": {
	# 				"ItemId": int(request.item_id),
	# 				"PrimaryCategory": request.attributes.get("primary_category", None),
	# 				"trialProduct": request.trial_product,
	# 				"Attributes": request.attributes
	# 				if request.attributes
	# 				else {
	# 					"name": "Updated Product",
	# 					"brand": "No Brand",
	# 					"short_description": request.attributes.get("short_description", ""),
	# 				},
	# 				"Skus": {
	# 					"Sku": [
	# 						{
	# 							"SkuId": int(sku.sku_id),
	# 							"SellerSku": sku.seller_sku,
	# 							"saleProp": {
	# 								"color_family": sku.color_family if sku.color_family else None,
	# 								"size": sku.size if sku.size else None,
	# 							}
	# 							if sku.color_family or sku.size
	# 							else None,
	# 							"Images": {"Image": sku.images} if sku.images else None,
	# 						}
	# 						for sku in request.skus
	# 					]
	# 				}
	# 				if request.skus
	# 				else None,
	# 			}
	# 		}
	# 	}
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaUpdateProductResponse(**response)

	# def update_sellable_quantity(self, skus: list[LazadaSkuStock]) -> LazadaUpdateSellableQuantityResponse:
	# 	path = "/product/stock/sellable/update"
	# 	payload = "".join([sku.to_xml(exclude_none=True).decode("utf-8") for sku in skus])
	# 	params = {"payload": f"<Request><Product><Skus>{payload}</Skus></Product></Request>"}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaUpdateSellableQuantityResponse(**response)

	# def upload_image(self, request: LazadaUploadImageRequest) -> LazadaUploadImageResponse:
	# 	path = "/image/upload"
	# 	with open(request.image_path, "rb") as image_file:
	# 		files = {"image": image_file}
	# 		response = self.client.make_request(path, params={}, method="POST", files=files)
	# 	return LazadaUploadImageResponse(**response)
