from datetime import datetime, timedelta, timezone

import requests

from .exceptions import PayooAPIException, PayooException, SignatureVerificationError
from .signature import SignatureHandler

BASE_URL = "https://mpos-partnergw-sbd.payoo.com.vn/mPOS_PartnerGatewayWCFService/REST/"


class PayooMPOSAPIClient:
	"""
	Client tầng thấp, chịu trách nhiệm gửi request, xử lý header và chữ ký.
	"""

	def __init__(
		self,
		username: str,
		credential_plain: str,
		private_key_pem: str,
		payoo_public_key_pem: str,
		account_name: str | None = None,
		base_url: str = BASE_URL,
	):
		self.account_name = account_name
		self.base_url = str(base_url).rstrip("/")
		self.username = username
		self.signature_handler = SignatureHandler(private_key_pem, payoo_public_key_pem)
		self.api_credential = self.signature_handler.hash_credential(credential_plain)

	def post(self, method_name: str, request_body_model):
		"""
		Thực hiện POST request tới một endpoint của Payoo.
		"""
		url = f"{self.base_url}/{method_name}"
		utc_plus_7 = timezone(timedelta(hours=7))
		request_time = datetime.now(utc_plus_7).strftime("%Y%m%d%H%M%S")

		json_body = request_body_model.model_dump_json(by_alias=True, exclude_none=True)
		signature = self.signature_handler.sign(json_body)

		headers = {
			"MerchantName": self.username,
			"Credential": self.api_credential,
			"RequestTime": request_time,
			"Signature": signature,
			"Content-Type": "text/plain; charset=utf-8",  # Chỉ định charset
		}

		try:
			response = requests.post(url, data=json_body.encode("utf-8"), headers=headers, timeout=30)
			result = response.json()
			response_signature = response.headers.get("Signature")

			# Xác thực chữ ký của response từ Payoo
			if response_signature:
				data_to_verify = f"{json_body}|{response.text}"

				verification_result = self.signature_handler.verify(response_signature, data_to_verify)

				if not verification_result:
					raise SignatureVerificationError("Chữ ký phản hồi từ Payoo không hợp lệ.")
			if result.get("ReturnCode") == -33:
				raise PayooException("Order does not exist")
			elif result.get("ReturnCode") != 0:
				raise PayooAPIException(result.get("Description", "Unknown error"), result.get("ReturnCode"))

			return result

		except requests.exceptions.RequestException as e:
			raise PayooAPIException(f"Lỗi kết nối đến Payoo: {e}")
