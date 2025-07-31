from inno_erp.libs.base_api import BaseApi

from .auth import TiktokShopAuthApi
from .category import TiktokShopCategoryAPI
from .client import TiktokShopClient
from .logictics import TiktokShopLogisticsAPI
from .order import TiktokShopOrderApi
from .product import TiktokShopProductAPI
from .shop import TiktokShopShopAPI

__all__ = ["TiktokShopApi", "TiktokShopAuthApi"]


class TiktokShopApi(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"category": TiktokShopCategoryAPI,
		"logictics": TiktokShopLogisticsAPI,
		"order": TiktokShopOrderApi,
		"product": TiktokShopProductAPI,
		"shop": TiktokShopShopAPI,
	}

	# Type hints for better IDE support
	category: TiktokShopCategoryAPI
	logictics: TiktokShopLogisticsAPI
	product: TiktokShopProductAPI
	order: TiktokShopOrderApi
	shop: TiktokShopShopAPI

	def __init__(
		self,
		access_token: str,
		app_key: str,
		app_secret: str,
		shop_cipher: str | None = None,
		shop_id: str | None = None,
	):
		self.client = TiktokShopClient(
			access_token=access_token,
			app_key=app_key,
			app_secret=app_secret,
			shop_cipher=shop_cipher,
			shop_id=shop_id,
		)
