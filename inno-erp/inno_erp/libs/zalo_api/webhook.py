import base64
import json

from .auth import AuthAPI
from .client import ZaloClient, verify_code_verifier
from .typing import ZaloAccessTokenResponse, ZaloException, ZaloMetadata


def access_token(
	oa_id: str, code: str, code_challenge: str, state: str, metadata: dict, secret_token: str
) -> ZaloAccessTokenResponse:
	"""
	Exchange the authorization code for an access token.

	Args:
		oa_id (str): The ID of the official account
		code (str): The authorization code
		code_challenge (str): The code challenge
		state (str): The state
		metadata (dict): The metadata
		secret_token (str): The secret token

	Returns:
		ZaloAccessTokenResponse: The access token

	Raises:
		ZaloException: If the code verifier is invalid
	"""
	app_id = base64.urlsafe_b64decode(state).decode("utf-8")

	meta = ZaloMetadata(**json.loads(metadata))
	meta.oa_id = oa_id

	if not verify_code_verifier(meta.code_verifier, code_challenge):
		raise ZaloException("Invalid code verifier")

	return AuthAPI(ZaloClient("BYPASS")).get_access_token(
		app_id, secret_token, code, meta.code_verifier
	), meta
