from inno_erp.libs.base_api import BaseApi

from .client import LazadaClient

# from .datamoat import LazadaDataMoat
# from .global_product import LazadaGlobalProduct
# from .im_chat import LazadaInstantMessaging
# from .media import LazadaMedia
# from .order import LazadaOrder
from .product import LazadaProductAPI

# from .product_review import LazadaReview
from .seller import LazadaSellerAPI

# from .store import LazadaStore
# from .voucher import LazadaSellerVoucher

__all__ = ["LazadaAPI", "LazadaAuthApi"]


class LazadaAPI(BaseApi):
	DOMAIN_APIS = {  # noqa: RUF012
		"product": LazadaProductAPI,
		# "order": LazadaOrder,
		"seller": LazadaSellerAPI,
		# "datamoat": LazadaDataMoat,
		# "global_product": LazadaGlobalProduct,
		# "product_review": LazadaReview,
		# "store": LazadaStore,
		# "media": LazadaMedia,
		# "im_chat": LazadaInstantMessaging,
		# "voucher": LazadaSellerVoucher,
	}

	# Type hints for better IDE support
	product: LazadaProductAPI
	# order: LazadaOrder
	seller: LazadaSellerAPI
	# datamoat: LazadaDataMoat
	# global_product: LazadaGlobalProduct
	# product_review: LazadaReview
	# store: LazadaStore
	# media: LazadaMedia
	# im_chat: LazadaInstantMessaging
	# voucher: LazadaSellerVoucher

	def __init__(self, access_token: str, app_key: str, app_secret: str):
		self.client = LazadaClient(access_token, app_key, app_secret)
