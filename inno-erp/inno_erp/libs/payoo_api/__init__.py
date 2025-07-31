from inno_erp.libs.base_api import BaseApi

from .client import PayooMPOSAPIClient
from .exceptions import PayooException
from .order import PayooOrderAPI

__all__ = ["PayooException", "PayooMPOS"]


class PayooMPOS(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"order": PayooOrderAPI,
	}

	order: PayooOrderAPI

	def __init__(
		self,
		username: str,
		account_name: str,
		credential_plain: str,
		private_key_path: str,
		payoo_public_key_path: str,
	):
		try:
			with open(private_key_path) as f:
				private_key_pem = f.read()
			with open(payoo_public_key_path) as f:
				payoo_public_key_pem = f.read()
		except FileNotFoundError as e:
			raise PayooException(f"Không tìm thấy file key: {e}")

		self.client = PayooMPOSAPIClient(
			username=username,
			account_name=account_name,
			credential_plain=credential_plain,
			private_key_pem=private_key_pem,
			payoo_public_key_pem=payoo_public_key_pem,
		)
