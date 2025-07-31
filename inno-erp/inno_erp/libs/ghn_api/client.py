import urllib.parse

import requests

from .exceptions import GhnException

BASE_URL = "https://dev-online-gateway.ghn.vn"
# BASE_URL = "https://online-gateway.ghn.vn"


class GhnClient:
	def __init__(
		self,
		access_token: str,
		base_url: str = BASE_URL,
		timeout: int = 30,
	):
		self.access_token = access_token
		self.base_url = str(base_url).rstrip("/")
		self.timeout = timeout

	def get_headers(self, content_type="application/json"):
		headers = {
			"Content-Type": content_type,
			"Token": self.access_token,
		}
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
			response.raise_for_status()

			if response.status_code == 200:
				result = response.json()
				if result.get("code") == 200:
					return result

				raise GhnException(
					code=result.get("code", 400),
					message=result.get("message", "Error from GHN"),
				)
			else:
				# Non-200 status code, try to get error details from response
				try:
					error_data = response.json()
					raise GhnException(
						code=error_data.get("code", 400),
						message=error_data.get("message", f"HTTP {response.status_code} Error"),
					)
				except ValueError:
					# Response is not valid JSON
					raise GhnException(
						code=response.status_code,
						message=f"HTTP {response.status_code}: {response.text}",
					)

		except requests.RequestException as e:
			# Network or request-related error
			raise GhnException(
				code=500,
				message=f"Request failed: {e!s}",
			) from e
