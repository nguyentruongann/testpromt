from .client import LazadaClient
from .typing import *


class LazadaSellerAPI:
	def __init__(self, client: LazadaClient):
		self.client = client

	def get_seller_info(self) -> LazadaGetSellerResponse:
		path = "/seller/get"
		response = self.client.make_request(path)
		return LazadaGetSellerResponse(**response)

	# def get_seller_metrics(self) -> LazadaGetSellerMetricsResponse:
	# 	path = "/seller/metrics/get"
	# 	response = self.client.make_request(path)
	# 	return LazadaGetSellerMetricsResponse(**response)

	# def get_pickup_store_list(self) -> LazadaGetPickupStoreListResponse:
	# 	path = "/rc/store/list/get"
	# 	response = self.client.make_request(path)
	# 	return LazadaGetPickupStoreListResponse(**response)

	# def get_seller_performance(
	# 	self, request: LazadaGetSellerPerformanceRequest
	# ) -> LazadaGetSellerPerformanceResponse:
	# 	path = "/seller/performance/get"
	# 	params = {"language": request.language}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetSellerPerformanceResponse(**response)

	# def get_warehouse_by_seller_id(self) -> LazadaGetWarehouseBySellerIdResponse:
	# 	path = "/rc/warehouse/get"
	# 	response = self.client.make_request(path)
	# 	print(response)
	# 	return LazadaGetWarehouseBySellerIdResponse(**response)

	# def query_warehouse_detail_info(self) -> LazadaQueryWarehouseDetailInfoResponse:
	# 	path = "/rc/warehouse/detail/get"
	# 	response = self.client.make_request(path)
	# 	return LazadaQueryWarehouseDetailInfoResponse(**response)

	# def get_seller_center_msg_list(
	# 	self, request: LazadaGetSellerCenterMsgListRequest
	# ) -> LazadaGetSellerCenterMsgListResponse:
	# 	path = "/sellercenter/msg/list"
	# 	params = {"language": request.language, "page": str(request.page), "pageSize": str(request.page_size)}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetSellerCenterMsgListResponse(**response)

	# def fetch_seller_policy(self, request: LazadaFetchSellerPolicyRequest) -> LazadaFetchSellerPolicyResponse:
	# 	path = "/seller/policy/fetch"
	# 	params = {"locale": request.locale}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaFetchSellerPolicyResponse(**response)

	# def sync_seller_config(self, request: LazadaSyncSellerConfigRequest) -> LazadaSyncSellerConfigResponse:
	# 	path = "/seller/ar/config/syn"
	# 	params = {"siteId": request.site_id, "source": request.source, "uid": str(request.seller_id)}

	# 	if request.contents is None:
	# 		params["contents"] = json.dumps([{"sku_id": "default", "config": "default"}])
	# 	else:
	# 		params["contents"] = json.dumps(request.contents)

	# 	if request.syn_date is None:
	# 		vn_tz = timezone(timedelta(hours=7))
	# 		params["synDate"] = datetime.now(vn_tz).strftime("%Y-%m-%dT%H:%M:%S+07:00")
	# 	else:
	# 		params["synDate"] = request.syn_date

	# 	if request.business:
	# 		params["business"] = request.business

	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaSyncSellerConfigResponse(**response)

	# def get_cross_border_countries(
	# 	self, request: LazadaGetCrossBorderCountriesRequest
	# ) -> LazadaGetCrossBorderCountriesResponse:
	# 	path = "/seller/cb/country/get"
	# 	params = {"type": request.type}
	# 	if request.seller_country:
	# 		params["seller_country"] = request.seller_country
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetCrossBorderCountriesResponse(**response)

	# def get_seller_register_info(
	# 	self, request: LazadaGetCrossBorderRegisterInfoRequest
	# ) -> LazadaGetCrossBorderRegisterInfoResponse:
	# 	path = "/seller/cb/register/info"
	# 	payload = [{"licenseNumber": request.license_number, "companyName": request.company_name}]
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetCrossBorderRegisterInfoResponse(**response)

	# def get_cross_border_country_locations(
	# 	self, request: LazadaGetCrossBorderCountryLocationsRequest
	# ) -> LazadaGetCrossBorderCountryLocationsResponse:
	# 	path = "/seller/cb/country/location/get"
	# 	params = {"location_id": str(request.location_id), "level": str(request.level)}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetCrossBorderCountryLocationsResponse(**response)

	# def get_cross_border_payment_config(
	# 	self, request: LazadaGetCrossBorderPaymentConfigRequest
	# ) -> LazadaGetCrossBorderPaymentConfigResponse:
	# 	path = "/seller/cb/payment/config"
	# 	params = {"payload": request.payload}
	# 	response = self.client.make_request(path, params=params)

	# 	if (
	# 		isinstance(response, dict)
	# 		and response.get("type") == "ISV"
	# 		and response.get("code") == "IncompleteSignature"
	# 	):
	# 		raise Exception(
	# 			"IncompleteSignature error: The request signature does not conform to platform standards"
	# 		)

	# 	return LazadaGetCrossBorderPaymentConfigResponse(**response)

	# def get_buybox_info(self, request: LazadaGetBuyboxInfoRequest) -> LazadaGetBuyboxInfoResponse:
	# 	path = "/hunting/buybox/get"
	# 	params = {"item_id": str(request.item_id), "sku_id": str(request.sku_id)}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaGetBuyboxInfoResponse(**response)

	# def save_warehouse_info(self, request: LazadaSaveWarehouseInfoRequest) -> LazadaSaveWarehouseInfoResponse:
	# 	path = "/rc/sellerWarehouse/saveWarehouseInfo"
	# 	warehouse_address_info = {
	# 		"locationLevel2Label": request.province_label,
	# 		"locationLevel3Label": request.city_label,
	# 		"locationLevel4Label": request.district_label,
	# 		"address": request.address,
	# 		"postalCode": request.postal_code,
	# 		"countryIosCode": "VN",
	# 		"defaultAddress": "0",
	# 	}
	# 	if request.latitude is not None:
	# 		warehouse_address_info["latitude"] = str(request.latitude)
	# 	if request.longitude is not None:
	# 		warehouse_address_info["longitude"] = str(request.longitude)

	# 	params = {
	# 		"ownerType": "0",
	# 		"sellerId": str(request.seller_id),
	# 		"warehouseOwnerType": "SELLER",
	# 		"warehouseContactDTO": json.dumps({"phoneNumber": request.phone_number, "email": request.email}),
	# 		"siteId": "VN",
	# 		"warehouseAddressInfoDTO": json.dumps(warehouse_address_info),
	# 		"warehouseType": "200",
	# 		"ownerId": str(request.seller_id),
	# 		"warehouseName": request.warehouse_name,
	# 		"currencyCode": "VND",
	# 		"resourceType": "1",
	# 	}
	# 	response = self.client.make_request(path, params=params, method="POST")
	# 	return LazadaSaveWarehouseInfoResponse(**response)

	# def check_cross_border_register_fields(
	# 	self, request: LazadaCheckCrossBorderRegisterFieldsRequest
	# ) -> LazadaCheckCrossBorderRegisterFieldsResponse:
	# 	path = "/seller/cb/register/fieldcheck"
	# 	payload = [
	# 		{"countryRegion": field["countryRegion"], "name": field["name"], "value": field["value"]}
	# 		for field in request.fields_to_verify
	# 	]
	# 	params = {"payload": json.dumps(payload)}
	# 	response = self.client.make_request(path, params=params)
	# 	return LazadaCheckCrossBorderRegisterFieldsResponse(**response)

	# def batch_query_shop_follow_status(
	# 	self, request: LazadaBatchQueryShopFollowStatusRequest
	# ) -> LazadaBatchQueryShopFollowStatusResponse:
	# 	path = "/shop/follow/status/batch/query"
	# 	params = {"buyer_ids": json.dumps(request.buyer_ids)}
	# 	response = self.client.make_request(path, params=params)

	# 	if isinstance(response, dict) and response.get("type") == "ISP" and response.get("code") == 3000002:
	# 		raise Exception("ISP error: follow status query fail")

	# 	if isinstance(response, dict) and "result" in response:
	# 		result_data = response["result"]
	# 		if isinstance(result_data, dict) and "result" in result_data:
	# 			response["result"] = result_data["result"]
	# 		else:
	# 			response["result"] = result_data
	# 	return LazadaBatchQueryShopFollowStatusResponse(**response)
