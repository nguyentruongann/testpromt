from .typing import FeeResponse, PriceRequest


class ViettelPostFeeApi:
	def __init__(self, client):
		self.client = client

	def get_price_nlp(self, price_request: PriceRequest):
		"""Calculate shipping price using NLP endpoint"""
		response = self.client.make_request(
			url="/v2/order/getPriceNlp", method="POST", json=price_request.model_dump()
		)
		return FeeResponse(**response)

	def calculate_delivery_rates(self, pickup_address, delivery_address, package_details):
		"""
		Calculate shipping rates for all 3 service types: Saving, Fast, Express
		Returns standardized format for delivery service comparison
		"""
		# Service type mapping for ViettelPost
		service_types = {
			"saving": "STK",  # Chuyển phát tiết kiệm
			"fast": "SCN",  # Chuyển phát nhanh
			"express": "SHT",  # Chuyển phát hỏa tốc
		}

		rates = {}
		sender_addr = pickup_address.get("address", "")
		receiver_addr = delivery_address.get("address", "")
		weight = int(package_details.get("weight", 1) * 1000)  # Convert kg to grams
		value = package_details.get("value", 0)
		cod_amount = package_details.get("cod_amount", 0)

		for service_name, service_code in service_types.items():
			try:
				price_request = PriceRequest(
					product_weight=weight,
					product_price=value,
					money_collection=cod_amount,
					order_service_add="",
					order_service=service_code,
					sender_address=sender_addr,
					receiver_address=receiver_addr,
				)

				fee_response = self.get_price_nlp(price_request)
				fee_data = fee_response.data

				if fee_data:
					# Estimate delivery time based on service type
					delivery_time_map = {
						"STK": "3-5",  # Economy
						"SCN": "2-3",  # Fast
						"SHT": "1-2",  # Express
					}

					rates[service_name] = {
						"price": fee_data.money_total,
						"estimated_days": delivery_time_map.get(service_code, "2-4"),
						"service_code": service_code,
						"provider": "VIETTELPOST",
					}
				else:
					rates[service_name] = None

			except Exception as e:
				# Log error but continue with other service types
				import frappe

				frappe.log_error(f"ViettelPost {service_name} rate calculation failed: {e!s}")
				rates[service_name] = None

		return rates

	def calculate_fee(self, params: dict):
		"""Calculate shipping fee (legacy method for compatibility)"""
		response = self.client.make_request(url="/api/v1.1/calculatefee", method="GET", params=params)
		return FeeResponse(**response)
