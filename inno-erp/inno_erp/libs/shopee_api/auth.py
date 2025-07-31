import hashlib
import hmac
import time

import requests

from .types.exceptions import APIError


class AuthAPI:
	def __init__(self, config: dict):
		self.config = config

	def _generate_signature(self, partner_id, path, timestamp, partner_key):
		base_string = f"{partner_id}{path}{timestamp}"
		return hmac.new(partner_key.encode(), base_string.encode(), hashlib.sha256).hexdigest()

	def get_auth_url_by_shop_id(self, shop_id: str) -> str:
		partner_id = self.config["partner_id"]
		partner_key = self.config["partner_key"]
		host = self.config["base_url"]
		path = "/api/v2/shop/auth_partner"
		redirect_url = self.config["callback_url"]
		timestamp = int(time.time())

		sign = self._generate_signature(partner_id, path, timestamp, partner_key)

		url = (
			f"{host}{path}?partner_id={partner_id}&timestamp={timestamp}&sign={sign}&redirect={redirect_url}"
		)
		return url

	def get_callback_token_by_shop_id(self, shop_id: int, code: str) -> dict:
		partner_id = self.config["partner_id"]
		partner_key = self.config["partner_key"]
		host = self.config["base_url"]
		path = "/api/v2/auth/token/get"
		timestamp = int(time.time())

		sign = self._generate_signature(partner_id, path, timestamp, partner_key)

		url = f"{host}{path}?partner_id={partner_id}&timestamp={timestamp}&sign={sign}"

		payload = {"code": code, "shop_id": int(shop_id), "partner_id": int(partner_id)}

		headers = {"Content-Type": "application/json"}
		response = requests.post(url, json=payload, headers=headers)

		print(response.json())

		if not response.ok:
			raise APIError(response.status_code, response.text)

		return response.json()
