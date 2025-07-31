import urllib.parse

import requests

from .exceptions import ViettelPostException

BASE_URL = "https://partner.viettelpost.vn"


class ViettelPostClient:
	def __init__(
		self,
		access_token: str,
		username: str = None,
		base_url: str = BASE_URL,
		timeout: int = 30,
	):
		self.access_token = access_token
		self.username = username
		self.base_url = str(base_url).rstrip("/")
		self.timeout = timeout

	def get_headers(self, content_type="application/json"):
		headers = {
			"Content-Type": content_type,
			"Token": self.access_token,
		}
		if self.username:
			headers["Username"] = self.username
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

			if response.status_code == 200:
				result = response.json()
				if result.get("status") == 200 and not result.get("error", False):
					return result

				# ViettelPost specific error response
				raise ViettelPostException(
					success=False,
					message=result.get("message", "Error from ViettelPost"),
					error_code=str(result.get("status", 400)),
					log_id="",
				)
			else:
				# Non-200 status code, try to get error details from response
				try:
					error_data = response.json()
					raise ViettelPostException(
						success=False,
						message=error_data.get("message", f"HTTP {response.status_code} Error"),
						error_code=str(response.status_code),
						log_id="",
					)
				except ValueError:
					# Response is not valid JSON
					raise ViettelPostException(
						success=False,
						message=f"HTTP {response.status_code}: {response.text}",
						error_code=str(response.status_code),
						log_id="",
					)

		except requests.RequestException as e:
			# Network or request-related error
			raise ViettelPostException(
				success=False,
				message=f"Request failed: {e!s}",
				error_code="REQUEST_ERROR",
				log_id="",
			) from e
