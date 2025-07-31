import json

import requests

from .typing import (
	ZaloAccessTokenResponse,
	ZaloException,
	ZaloResponse,
	ZaloResponseType,
)

ATTACHMENT_MAP = {
	"image": "Image",
	"gif": "Gif",
	"sticker": "Sticker",
	"link": "Link",
}


class ZaloClient:
	access_token: str

	def __init__(self, access_token: str, base_url: str = "https://openapi.zalo.me"):
		self.access_token = access_token
		self.base_url = base_url

	def get_headers(self, content_type: str = "application/json"):
		return {
			"Content-Type": content_type,
			"access_token": self.access_token,
		}

	def make_request(
		self,
		path: str,
		method: str,
		json: dict | None = None,
		data: dict | None = None,
		headers: dict | None = None,
		params: dict | None = None,
		typing: type[ZaloResponseType] = ZaloResponse,
	) -> ZaloResponseType:
		if not headers:
			headers = self.get_headers("application/json" if json else "application/x-www-form-urlencoded")

		full_url = self.base_url + path
		if path.startswith("http://") or path.startswith("https://"):
			full_url = path

		response = requests.request(method, full_url, headers=headers, json=json, data=data, params=params)
		if response.status_code == 200:
			resp = response.json()
			if issubclass(typing, ZaloResponse):
				if resp.get("error") == 0:
					return typing(**resp)
				else:
					raise ZaloException(resp["message"], resp["error"])
			elif issubclass(typing, ZaloAccessTokenResponse):
				return typing(**resp)
		else:
			raise ZaloException(response.text, response.status_code)

	def upload(self, type, file_name, file_binary) -> ZaloResponse:
		"""
		Upload an attachment (image/file) to Zalo Official Account.

		Args:
		    type (str): Type of attachment to upload ('image' or 'file')
		    file_name (str): Name of the file being uploaded
		    file_binary (bytes): Binary content of the file to upload

		Returns:
		    ZaloResponse: Response containing the attachment_id if successful

		Raises:
		    ZaloException: If upload fails or API returns an error
		"""
		headers = {
			"access_token": self.access_token,
		}
		files = {
			"file": (file_name, file_binary),
		}

		response = requests.post(self.base_url + "/v2.0/oa/upload/", headers=headers, files=files)
		if response.status_code == 200:
			resp = response.json()
			if resp.get("error") == 0:
				return ZaloResponse(**resp)
			else:
				raise ZaloException(resp["message"], resp["error"])
		else:
			raise ZaloException(response.text, response.status_code)


def generate_code_verifier():
	import base64
	import hashlib
	import os

	# Generate a random code verifier
	code_verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")

	# Generate the code challenge using SHA256
	code_challenge = (
		base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
		.decode("utf-8")
		.rstrip("=")
	)

	return code_verifier, code_challenge


# Authentication URL
def get_auth_url(app_id, redirect_uri):
	import base64
	import urllib.parse

	code_verifier, code_challenge = generate_code_verifier()
	auth_url = (
		f"https://oauth.zaloapp.com/v4/oa/permission?app_id={app_id}&redirect_uri={urllib.parse.quote(redirect_uri, safe='')}"
		f"&code_challenge={code_challenge}&state={base64.urlsafe_b64encode(app_id.encode('utf-8')).decode('utf-8')}"
	)
	return auth_url, code_verifier


def get_mac(app_id, data, timestamp, secret_key):
	import hashlib
	import hmac

	# Create the message to be hashed
	message = f"{app_id}{data}{timestamp}{secret_key}".encode()

	# Create the HMAC object using SHA256
	hmac_object = hmac.new(secret_key.encode("utf-8"), message, hashlib.sha256)

	# Get the hexadecimal digest of the HMAC
	mac = hmac_object.hexdigest()

	return mac


def build_mac_for_authentication(app_id: str, data: str, timestamp: str, secret_key: str) -> str:
	import hashlib

	res = "".join([app_id, data, timestamp, secret_key])
	return f"mac={hashlib.sha256(res.encode('utf-8')).hexdigest()}"


def verify_signature(payload: dict, signature: str, oa_secret: str) -> bool:
	del payload["cmd"]
	data_json = json.dumps(payload, separators=(",", ":"))
	expected_signature = build_mac_for_authentication(payload.app_id, data_json, payload.timestamp, oa_secret)
	return signature == expected_signature


# Verify the code verifier and code challenge
def verify_code_verifier(code_verifier, code_challenge):
	import base64
	import hashlib

	# Generate the code challenge from the code verifier
	generated_code_challenge = (
		base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
		.decode("utf-8")
		.rstrip("=")
	)

	# Compare the generated code challenge with the original one
	return generated_code_challenge == code_challenge
