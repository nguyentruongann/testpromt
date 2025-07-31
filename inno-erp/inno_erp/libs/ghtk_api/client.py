import urllib.parse

import requests

from .exceptions import GhtkException

BASE_URL = "https://services-staging.ghtklab.com"
# BASE_URL = "https://services.giaohangtietkiem.vn"


class GhtkClient:
	def __init__(
		self,
		partner_code: str | None,
		access_token: str,
		base_url: str = BASE_URL,
		timeout: int = 30,
	):
		self.partner_code = partner_code
		self.access_token = access_token
		self.base_url = str(base_url).rstrip("/")
		self.timeout = timeout

	def get_headers(self, content_type="application/json"):
		headers = {
			"Content-Type": content_type,
			"Token": self.access_token,
		}

		if self.partner_code:
			headers["X-Client-Source"] = self.partner_code

		return headers

	def make_request(
		self,
		url: str,
		method: str,
		json: dict | None = None,
		params: dict | None = None,
		headers: dict | None = None,
	) -> dict:
		if not headers:
			headers = self.get_headers()

		# encode url-encoded params
		encoded_params = (
			urllib.parse.urlencode(params, encoding="utf-8", quote_via=urllib.parse.quote) if params else None
		)

		try:
			response = requests.request(
				method,
				self.base_url + url,
				headers=headers,
				json=json,
				params=encoded_params,
				timeout=self.timeout,
			)

			result = response.json()
			if response.status_code >= 200 and response.status_code < 300 and result.get("success"):
				return result

				# API returned success=false, raise exception with API error details
			raise GhtkException(
				success=result.get("success"),
				message=result.get("message", "Error from GHTK"),
				error_code=result.get("error_code", "0"),
				log_id=result.get("log_id", ""),
			)

		except ValueError:
			# Response is not valid JSON
			raise GhtkException(
				success=False,
				message=f"HTTP {response.status_code}: {response.text}",
				error_code=result.get("error_code", "0"),
				log_id=result.get("log_id", ""),
			)
		except requests.RequestException as e:
			# Network or request-related error
			raise GhtkException(
				success=False,
				message=f"Request failed: {e!s}",
				error_code="REQUEST_ERROR",
			) from e
