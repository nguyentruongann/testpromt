import hashlib
import hmac
import time

import requests

from .exceptions import LazadaException

BASE_URL = "https://api.lazada.vn/rest"


class LazadaClient:
	def __init__(
		self,
		access_token: str,
		app_key: str,
		app_secret: str,
		base_url=BASE_URL,
	):
		self.access_token = access_token
		self.app_key = app_key
		self.app_secret = app_secret
		self.base_url = base_url.rstrip("/")

	def _generate_signature(self, path: str, params: dict[str, str]) -> str:
		sorted_params = sorted(params.items())
		parameters_str = path + "".join(f"{k}{v}" for k, v in sorted_params)
		return hmac.new(self.app_secret.encode(), parameters_str.encode(), hashlib.sha256).hexdigest().upper()

	def make_request(
		self,
		path: str,
		params: dict[str, str] | None = None,
		method: str = "GET",
		body: dict[str, any] | None = None,
		files: dict[str, any] | None = None,
		required_auth: bool = True,
	) -> dict[str, any]:
		if params is None:
			params = {}

		params["app_key"] = self.app_key
		params["timestamp"] = str(int(time.time() * 1000))
		params["sign_method"] = "sha256"

		if required_auth:
			params["access_token"] = self.access_token

		params["sign"] = self._generate_signature(path, params)

		url = f"{self.base_url}{path}"

		try:
			if method.upper() == "GET":
				response = requests.get(url, params=params)
			elif method.upper() == "POST":
				if files:
					response = requests.post(url, params=params, files=files)
				else:
					headers = {"Content-Type": "application/json"}
					response = requests.post(url, params=params, json=body, headers=headers)
			else:
				raise ValueError(f"Unsupported method: {method}")

			response.raise_for_status()

			result = response.json()

			# Check for Lazada API errors in the response
			if result.get("code") == "0" or result.get("success") is True:
				return result
			elif result.get("code") and result.get("code") != "0":
				raise LazadaException(
					success=False,
					message=result.get("message", "API Error"),
					error_code=result.get("code", ""),
					request_id=result.get("request_id", ""),
					http_status_code=response.status_code,
					error=result,
				)
			else:
				return result

		except requests.RequestException as e:
			raise LazadaException(
				success=False,
				message=f"HTTP Request failed: {e!s}",
				error_code="HTTP_ERROR",
				http_status_code=getattr(e.response, "status_code", None) if hasattr(e, "response") else None,
				error={"original_error": str(e)},
			)
