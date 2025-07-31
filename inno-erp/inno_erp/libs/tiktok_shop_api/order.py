# import time

# from typing import List, Optional
# from pydantic import ValidationError

from .client import TiktokShopClient

# from .typing import (
# 	TiktokShopCancelOrderRequest,
# 	TiktokShopCancelOrderResponse,
# 	TiktokShopGetOrderDetailsResponse,
# 	TiktokShopGetOrderListResponse,
# 	TiktokShopGetPriceDetailResponse,
# 	TiktokShopGetWarehouseListResponse,
# 	TiktokShopSkuCancelRequest,
# )


class TiktokShopOrderApi:
	def __init__(self, client: TiktokShopClient):
		self.client = client

	# def get_order_list(self, shop_cipher: str, page: int = 1, page_size: int = 20, locale: str = None):
	# 	params = {"shop_cipher": shop_cipher, "page": page, "page_size": page_size}
	# 	if locale:
	# 		params["locale"] = locale
	# 	return self.client.make_request("POST", Config.API_MAP["GET_ORDER_LIST"], params=params)

	# def get_order_detail(self, ids: list[str], shop_cipher: str, locale: str | None = None):
	# 	params = {"ids": ",".join(ids), "shop_cipher": shop_cipher}
	# 	if locale:
	# 		params["locale"] = locale
	# 	return self.client.make_request("GET", Config.API_MAP["GET_ORDER_DETAIL"], params=params)

	# def get_price_details(self, order_id: str, shop_cipher: str, locale: str | None = None):
	# 	params = {"order_id": order_id, "shop_cipher": shop_cipher}
	# 	if locale:
	# 		params["locale"] = locale
	# 	url = f"{Config.API_MAP['GET_PRICE_DETAILS']}/{order_id}/price_detail"
	# 	return self.client.make_request("GET", url, params=params)

	# def cancel_order(self, order_id: str, shop_cipher: str, product_body):
	# 	params = {"shop_cipher": shop_cipher}

	# 	try:
	# 		response = self.client.make_request(
	# 			"POST", Config.API_MAP["CANCEL_ORDER"], params=params, body=product_body
	# 		)
	# 		return response
	# 	except Exception as e:
	# 		raise Exception(f"Lỗi khi gửi yêu cầu hủy đơn hàng: {e}")
