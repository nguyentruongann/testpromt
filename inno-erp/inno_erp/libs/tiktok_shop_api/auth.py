import requests

from .typing import TiktokShopAuthResponse


class TiktokShopAuthApi:
	def __init__(self, app_key: str, app_secret: str) -> None:
		self.app_key = app_key
		self.app_secret = app_secret

	def get_access_token(self, auth_code: str):
		params = {
			"app_key": self.app_key,
			"app_secret": self.app_secret,
			"auth_code": auth_code,
			"grant_type": "authorized_code",
		}
		response = requests.get("https://auth.tiktok-shops.com/api/v2/token/get", params=params)
		response.raise_for_status()
		return TiktokShopAuthResponse(**response.json())
