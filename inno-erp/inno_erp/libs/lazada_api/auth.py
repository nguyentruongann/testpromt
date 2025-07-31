import hashlib
import hmac
import time

import requests

from .typing import LazadaAuthResponse

AUTH_URL = "https://auth.lazada.com/rest"


class LazadaAuthApi:
	def __init__(self, app_key: str, app_secret: str):
		self.app_key = app_key
		self.app_secret = app_secret
		# self.open_id: str | None = None

	def _generate_signature(self, path: str, params: dict) -> str:
		sorted_params = sorted(params.items())
		concat_str = path + "".join(f"{k}{v}" for k, v in sorted_params)
		return hmac.new(self.app_secret.encode(), concat_str.encode(), hashlib.sha256).hexdigest().upper()

	def get_access_token(self, code: str) -> LazadaAuthResponse:
		path = "/auth/token/create"
		params = {
			"app_key": self.app_key,
			"sign_method": "sha256",
			"timestamp": str(int(time.time() * 1000)),
			"code": code,
		}
		params["sign"] = self._generate_signature(path, params)
		response = requests.get(f"{AUTH_URL}{path}", params=params)
		response.raise_for_status()
		data = response.json()

		if data.get("code") != "0":
			raise Exception(f"Failed to get access token: {data.get('message')}")

		return LazadaAuthResponse(**data)

	def refresh_access_token(self, refresh_token) -> LazadaAuthResponse:
		path = "/auth/token/refresh"
		params = {
			"app_key": self.app_key,
			"sign_method": "sha256",
			"timestamp": str(int(time.time() * 1000)),
			"refresh_token": refresh_token,
		}
		params["sign"] = self._generate_signature(path, params)
		response = requests.get(f"{AUTH_URL}{path}", params=params)
		response.raise_for_status()
		data = response.json()

		if data.get("code") != "0":
			raise Exception(f"Failed to refresh token: {data.get('message')}")

		return LazadaAuthResponse(**data)

	# def get_access_token_with_open_id(self, open_id: str, auth_type: str) -> LazadaAuthResponse:
	# 	path = "/auth/token/createWithOpenId"
	# 	params = {
	# 		"app_key": self.app_key,
	# 		"sign_method": "sha256",
	# 		"timestamp": str(int(time.time() * 1000)),
	# 		"open_id": open_id,
	# 		"auth_type": auth_type,
	# 	}
	# 	params["sign"] = self._generate_signature(path, params)
	# 	response = requests.get(f"{AUTH_URL}{path}", params=params)
	# 	response.raise_for_status()
	# 	data = response.json()

	# 	if data.get("code") != "0":
	# 		raise Exception(f"Failed to get access token with open_id: {data.get('message')}")

	# 	self.access_token = data.get("access_token")
	# 	self.refresh_token = data.get("refresh_token")
	# 	self.expiry_time = time.time() + data.get("expires_in", 0)
	# 	self.open_id = open_id

	# 	return LazadaAuthResponse(**data)

	def is_token_expired(self) -> bool:
		return time.time() >= self.expiry_time

	def ensure_valid_token(self) -> str:
		if self.access_token and not self.is_token_expired():
			return self.access_token

		if not self.refresh_token:
			raise Exception("No refresh token available. Please authenticate again.")

		self.refresh_access_token()

		if not self.access_token:
			raise Exception("Failed to obtain a valid access token after refresh.")

		return self.access_token
