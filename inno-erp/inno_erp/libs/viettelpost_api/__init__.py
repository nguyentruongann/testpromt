from ..base_api import BaseApi
from .client import ViettelPostClient
from .exceptions import ViettelPostException
from .fee import ViettelPostFeeApi
from .order import ViettelPostOrderApi
from .auth import ViettelPostAuthApi
from .user import ViettelPostUserApi
from .service import ViettelPostServiceApi

__all__ = ["ViettelPostApi", "ViettelPostException"]


class ViettelPostApi(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"auth": ViettelPostAuthApi,
		"user": ViettelPostUserApi,
		"service": ViettelPostServiceApi,
		"order": ViettelPostOrderApi,
		"fee": ViettelPostFeeApi,
	}

	auth: ViettelPostAuthApi
	user: ViettelPostUserApi
	service: ViettelPostServiceApi
	order: ViettelPostOrderApi
	fee: ViettelPostFeeApi

	def __init__(self, access_token: str, username: str = None):
		self.client = ViettelPostClient(
			access_token=access_token,
			username=username,
		)

