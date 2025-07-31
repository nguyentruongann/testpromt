from ..base_api import BaseApi
from .address import GhtkAddressApi
from .b2c import GhtkB2CApi
from .client import GhtkClient
from .exceptions import GhtkException
from .order import GhtkOrderAPI

__all__ = ["GhtkAPI", "GhtkException"]


class GhtkApi(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"b2c": GhtkB2CApi,
		"order": GhtkOrderAPI,
		"address": GhtkAddressApi,
	}

	order: GhtkOrderAPI
	b2c: GhtkB2CApi
	address: GhtkAddressApi

	def __init__(self, access_token: str, partner_code: str | None = None):
		self.client = GhtkClient(
			partner_code=partner_code,
			access_token=access_token,
		)
