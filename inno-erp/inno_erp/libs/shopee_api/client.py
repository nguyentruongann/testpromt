import hashlib
import hmac
import time

import requests

from .types.exceptions import APIError


class ShopeeClient:
	def __init__(
		self,
		partner_id,
		partner_key,
		shop_id,
		access_token,
		base_url="https://partner.shopeemobile.com/api/v2",
	):
		self.partner_id = partner_id
		self.partner_key = partner_key.encode("utf-8")
		self.shop_id = shop_id
		self.access_token = access_token
		self.base_url = base_url

	def _gen_signature(self, path, timestamp):
		base_string = f"{self.partner_id}{path}{timestamp}"

		if self.access_token:
			base_string += f"{self.access_token}{self.shop_id}"
		return hmac.new(
			self.partner_key,
			base_string.encode("utf-8"),
			hashlib.sha256,
		).hexdigest()

	def make_request(self, method, path, params=None, data=None, files=None):
		timestamp = int(time.time())
		signature = self._gen_signature(path, timestamp)

		url = f"{self.base_url}{path}"

		query = {
			"partner_id": self.partner_id,
			"timestamp": timestamp,
			"sign": signature,
			"shop_id": self.shop_id,
			"access_token": self.access_token,
		}

		if files:
			headers = {}
		else:
			headers = {"Content-Type": "application/json"}

		if files:
			response = requests.request(
				method=method,
				url=url,
				headers=headers,
				params={**query, **(params or {})},
				data=data,
				files=files,
			)
		else:
			response = requests.request(
				method=method,
				url=url,
				headers=headers,
				params={**query, **(params or {})},
				json=data,
			)

		if not response.ok:
			raise APIError(response.status_code, response.text)

		return response.json()
