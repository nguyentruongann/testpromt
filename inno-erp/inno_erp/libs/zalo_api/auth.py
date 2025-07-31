from .client import ZaloClient
from .typing import ZaloAccessTokenResponse, ZaloException


class AuthAPI:
	def __init__(self, client: ZaloClient):
		self.client = client

	def get_access_token(
		self,
		app_id,
		secret_key,
		code=None,
		code_verifier=None,
		grant_type="authorization_code",
		refresh_token=None,
	) -> ZaloAccessTokenResponse:
		"""
		Get the access token for the official account.

		Args:
			app_id (str): The ID of the app
			secret_key (str): The secret key
			code (str): The authorization code
			code_verifier (str): The code verifier
			grant_type (str): The grant type
			refresh_token (str): The refresh token

		Returns:
			ZaloAccessTokenResponse: The access token

		Raises:
			ZaloException: If the app ID or secret key is not provided
			ZaloException: If the refresh token is required for refresh_token grant type
		"""
		if not app_id:
			raise ZaloException("App ID is required")
		if not secret_key:
			raise ZaloException("Secret key is required")

		headers = {
			"Content-Type": "application/x-www-form-urlencoded",
			"secret_key": secret_key,
		}

		if grant_type == "refresh_token":
			if not refresh_token:
				raise ZaloException("Refresh token is required for refresh_token grant type")
			data = {
				"app_id": app_id,
				"refresh_token": refresh_token,
				"grant_type": grant_type,
			}
		else:
			data = {
				"app_id": app_id,
				"code": code,
				"grant_type": grant_type,
				"code_verifier": code_verifier,
			}

		return self.client.make_request(
			"https://oauth.zaloapp.com/v4/oa/access_token",
			"POST",
			data=data,
			headers=headers,
			typing=ZaloAccessTokenResponse,
		)
