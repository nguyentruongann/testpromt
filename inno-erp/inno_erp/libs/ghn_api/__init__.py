from ..base_api import BaseApi
from .client import GhnClient
from .exceptions import GhnException
from .fee import GhnFeeApi
from .store import GhnStoreApi

__all__ = ["GhnAPI", "GhnException"]


class GhnApi(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"store": GhnStoreApi,
		"fee": GhnFeeApi,
	}

	store: GhnStoreApi
	fee: GhnFeeApi

	def __init__(self, access_token: str):
		self.client = GhnClient(
			access_token=access_token,
		)
