from .client import TiktokShopClient

# from .config import Config
from .typing import (
	# TikCreateProductResponse,
	TiktokShopCheckListingPrerequisitesResponse,
	TiktokShopCreateProductRequest,
	TiktokShopGetAttributesResponse,
	TiktokShopGetBrandsResponse,
	TiktokShopGetProductDetailResponse,
	TiktokShopSearchProductsResponse,
)


class TiktokShopProductAPI:
	def __init__(self, client: TiktokShopClient):
		self.client = client

	# def get_products(self, shop_cipher, product_ids):
	# 	params = {"shop_cipher": shop_cipher}

	# 	if isinstance(product_ids, str):
	# 		product_ids = [product_ids]
	# 	elif not isinstance(product_ids, list) or not all(isinstance(pid, (str, int)) for pid in product_ids):
	# 		raise ValueError("product_ids must be a string or a list of strings/integers")

	# 	responses = []
	# 	base_url = Config.API_MAP["GET_PRODUCTS"]
	# 	for product_id in product_ids:
	# 		url = f"{base_url}/{product_id}"
	# 		response = self.client.make_request("GET", url, params=params)
	# 		responses.append(response)

	# 	return responses[0] if len(responses) == 1 else responses

	# def search_products(
	# 	self,
	# 	shop_cipher,
	# 	page_size=10,
	# 	status=None,
	# 	seller_skus=None,
	# 	create_time_ge=None,
	# 	create_time_le=None,
	# 	update_time_ge=None,
	# 	update_time_le=None,
	# 	page_token=None,
	# 	category_version=None,
	# ):
	# 	params = {"shop_cipher": shop_cipher, "page_size": page_size}

	# 	if page_token:
	# 		params["page_token"] = page_token
	# 	if category_version:
	# 		params["category_version"] = category_version
	# 	body = {}
	# 	if status:
	# 		body["status"] = status

	# 	if seller_skus:
	# 		body["seller_skus"] = seller_skus
	# 	if create_time_ge is not None:
	# 		body["create_time_ge"] = create_time_ge
	# 	if create_time_le is not None:
	# 		body["create_time_le"] = create_time_le
	# 	if update_time_ge is not None:
	# 		body["update_time_ge"] = update_time_ge
	# 	if update_time_le is not None:
	# 		body["update_time_le"] = update_time_le

	# 	response = self.client.make_request(
	# 		"POST", Config.API_MAP["SEARCH_PRODUCTS"], params=params, body=body or None
	# 	)
	# 	return response

	# def get_list_product(self, shop_cipher, page_size=20):
	# 	product_ids = []
	# 	total_count = None
	# 	next_page_token = None

	# 	while True:
	# 		search_result = self.search_products(shop_cipher, page_size, page_token=next_page_token)
	# 		products = search_result.get("products", [])

	# 		if total_count is None:
	# 			total_count = search_result.get("total_count", 0)
	# 			print(f"Total products to retrieve: {total_count}")

	# 		product_ids.extend([product.get("id") for product in products if product.get("id")])

	# 		if len(product_ids) >= total_count:
	# 			print(f"Reached or exceeded total_count ({len(product_ids)} >= {total_count}). Stopping.")
	# 			break
	# 		if not products:
	# 			print("No more products in response. Stopping.")
	# 			break
	# 		next_page_token = search_result.get("next_page_token")

	# 	detailed_products = self.get_products(shop_cipher, product_ids)

	# 	return detailed_products

	# def create_product(self, shop_cipher, product_body):
	# 	params = {"shop_cipher": shop_cipher}

	# 	if not isinstance(product_body, dict):
	# 		raise ValueError("product_body phải là một dictionary")

	# 	required_fields = ["description", "category_id", "main_images", "skus"]
	# 	for field in required_fields:
	# 		if field not in product_body:
	# 			raise ValueError(f"Trường bắt buộc '{field}' không được cung cấp trong product_body")

	# 	if not isinstance(product_body["main_images"], list) or not product_body["main_images"]:
	# 		raise ValueError("main_images phải là một danh sách không rỗng")
	# 	if len(product_body["main_images"]) > 9:
	# 		raise ValueError("main_images chỉ được chứa tối đa 9 hình ảnh")
	# 	for image in product_body["main_images"]:
	# 		if not isinstance(image, dict) or "uri" not in image:
	# 			raise ValueError("Mỗi main_images phải là một dictionary chứa trường 'uri'")

	# 	if not isinstance(product_body["skus"], list) or not product_body["skus"]:
	# 		raise ValueError("skus phải là một danh sách không rỗng")

	# 	for sku in product_body["skus"]:
	# 		if "price" not in sku or not isinstance(sku["price"], dict):
	# 			raise ValueError("Mỗi SKU phải chứa trường 'price' là một dictionary")
	# 		if "inventory" not in sku or not isinstance(sku["inventory"], list) or not sku["inventory"]:
	# 			raise ValueError("Mỗi SKU phải chứa danh sách 'inventory' không rỗng")
	# 		for inventory in sku["inventory"]:
	# 			if "warehouse_id" not in inventory:
	# 				raise ValueError("Mỗi inventory trong SKU phải chứa trường 'warehouse_id'")

	# 	base_url = Config.API_MAP["CREATE_PRODUCT"]

	# 	response = self.client.make_request("POST", base_url, params=params, body=product_body)

	# 	return response

	# def get_brands(
	# 	self,
	# 	shop_cipher,
	# 	page_size,
	# 	category_id=None,
	# 	is_authorized=None,
	# 	brand_name=None,
	# 	page_token=None,
	# 	category_version=None,
	# ):
	# 	params = {"shop_cipher": shop_cipher, "page_size": page_size}
	# 	if category_id:
	# 		params["category_id"] = category_id
	# 	if is_authorized is not None:
	# 		params["is_authorized"] = int(is_authorized)
	# 	if brand_name:
	# 		params["brand_name"] = brand_name
	# 	if page_token:
	# 		params["page_token"] = page_token
	# 	if category_version:
	# 		params["category_version"] = category_version
	# 	return self.client.make_request("GET", Config.API_MAP["GET_BRANDS"], params=params)

	# def create_brand(self, brand_name):
	# 	"""Tạo một thương hiệu mới trong TikTok Shop."""
	# 	if not brand_name or not isinstance(brand_name, str):
	# 		raise ValueError("brand_name phải là chuỗi không rỗng")

	# 	body = {"name": brand_name}

	# 	response = self.client.make_request(
	# 		"POST", Config.API_MAP["CREATE_CUSTOM_BRAND"], params={}, body=body
	# 	)
	# 	return response

	# def get_attributes(self, shop_cipher, category_id, locale=None, category_version=None):
	# 	"""Lấy thuộc tính sản phẩm và bán hàng cho danh mục."""
	# 	params = {"shop_cipher": shop_cipher}
	# 	if locale:
	# 		params["locale"] = locale
	# 	if category_version:
	# 		params["category_version"] = category_version

	# 	url = f"{Config.API_MAP['GET_ATTRIBUTES']}/{category_id}/attributes"
	# 	return self.client.make_request("GET", url, params=params)

	# def get_prerequisites(self, shop_cipher, locale=None, category_version=None):
	# 	params = {"shop_cipher": shop_cipher}
	# 	return self.client.make_request(
	# 		"GET", Config.API_MAP["GET_CHECK_LISTING_PREREQUISITES"], params=params
	# 	)
