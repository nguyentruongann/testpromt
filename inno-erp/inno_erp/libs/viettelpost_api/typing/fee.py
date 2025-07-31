from pydantic import BaseModel

from .auth import ViettelPostResponse


class PriceRequest(BaseModel):
	product_weight: int  # in grams
	product_price: float
	money_collection: float
	order_service_add: str
	order_service: str
	sender_address: str
	receiver_address: str
	product_type: str = "HH"
	national_type: int = 1


class FeeData(BaseModel):
	money_total_old: float
	money_total: float
	money_total_fee: float
	money_fee: float
	money_collection_fee: float
	money_other_fee: float
	money_vas: float
	money_vat: float
	kpi_ht: float
	exchange_weight: int


class FeeResponse(ViettelPostResponse):
	data: FeeData | None = None
