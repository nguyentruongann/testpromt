import hashlib
import hmac
import json
import time

import requests
from pydantic.networks import HttpUrl

BASE_URL = "https://open-api.tiktokglobalshop.com"


class TikTokShopAPIException(Exception):
	"""Custom exception for TikTok Shop API errors."""

	def __init__(self, code: int, message: str, request_id: str = "N/A", details: dict | None = None):
		self.code = code
		self.message = message
		self.request_id = request_id
		self.details = details or {}
		super().__init__(f"API Error [Code {code}]: {message} (Request ID: {request_id})")


class TiktokShopClient:
	def __init__(
		self,
		access_token: str | None = None,
		app_key: str | None = None,
		app_secret: str | None = None,
		shop_cipher: str | None = None,
		shop_id: str | None = None,
		base_url: HttpUrl | str = BASE_URL,
		timeout: int = 30,
	):
		self.app_key = app_key
		self.app_secret = app_secret
		self.access_token = access_token
		self.shop_cipher = shop_cipher
		self.shop_id = shop_id
		self.base_url = str(base_url).rstrip("/")
		self.timeout = timeout

	def generate_signature(
		self,
		path: str,
		params: dict[str, any],
		body_content: dict | None = None,
		content_type: str = "application/json",
	) -> str:
		sign_params = params.copy()
		sign_params.pop("sign", None)

		sorted_params = sorted(sign_params.items())

		concatenated_params = "".join([f"{k}{v}" for k, v in sorted_params])

		normalized_path = path if path.startswith("/") else "/" + path

		base_string_parts = [self.app_secret, normalized_path, concatenated_params]

		if content_type != "multipart/form-data" and body_content:
			body_string = json.dumps(body_content) if isinstance(body_content, dict) else str(body_content)
			base_string_parts += body_string

		base_string_parts.append(self.app_secret)
		base_string = "".join(base_string_parts)

		return hmac.new(
			self.app_secret.encode("utf-8"), base_string.encode("utf-8"), hashlib.sha256
		).hexdigest()

	def make_request(
		self,
		path: str,
		params: dict[str, any] | None = None,
		method: str = "GET",
		body: dict[str, any] | None = None,
		form_data: dict[str, any] | None = None,
		headers: dict[str, any] | None = None,
		requires_auth: bool = True,
		requires_shop_context: bool = False,
	):
		"""Gửi yêu cầu đến API TikTok."""
		if params is None:
			params = {}

		# Xử lý headers
		headers = headers or {}
		headers["content-type"] = (
			"application/json"
			if body
			else "multipart/form-data"
			if form_data
			else headers.get("content-type", "application/json")
		)

		if requires_auth:
			headers["x-tts-access-token"] = self.access_token

		# Xử lý tham số truy vấn
		common_params = {
			"app_key": self.app_key,
			"timestamp": str(int(time.time())),
		}

		final_query_params = common_params.copy()

		if requires_shop_context:
			if not self.shop_cipher:
				raise ValueError("Shop context (shop_cipher) is required but not configured.")
			final_query_params["shop_cipher"] = self.shop_cipher

		if params:
			final_query_params.update(params)

		# Tạo chữ ký
		signature = self.generate_signature(
			path,
			final_query_params.copy(),
			body_content=body if body else form_data,
			content_type=headers["content-type"],
		)
		final_query_params["sign"] = signature

		# Tạo URL
		url = f"{self.base_url}{path}"

		try:
			response = requests.request(
				method=method.upper(),
				url=url,
				params=final_query_params,
				json=body if body else None,
				data=form_data if form_data else None,
				headers=headers,
			)
			response.raise_for_status()
			response_json = response.json()

			if response_json.get("code") != 0:
				raise TikTokShopAPIException(
					code=response_json.get("code"),
					message=response_json.get("message", "Unknown API error"),
					request_id=response_json.get("request_id", "N/A"),
					details=response_json.get("data"),
				)

			return response_json

		except requests.exceptions.HTTPError as e:
			error_data = e.response.json()
			raise TikTokShopAPIException(
				code=error_data.get("code", e.response.status_code),
				message=error_data.get("message", str(e)),
				request_id=error_data.get("request_id", "N/A"),
				details=error_data.get("data"),
			) from e
		except Exception as e:
			raise TikTokShopAPIException(code=-1, message=str(e), request_id="N/A") from e
