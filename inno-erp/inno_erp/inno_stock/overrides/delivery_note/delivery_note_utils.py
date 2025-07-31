import concurrent.futures
import hashlib
import json
import threading
import time
from typing import Dict, List, Literal, Optional

import frappe
from frappe import _
from pydantic import BaseModel

from inno_erp.libs.ghn_api import GhnApi
from inno_erp.libs.ghn_api.typing import GhnFeeRequest
from inno_erp.libs.ghtk_api import GhtkApi
from inno_erp.libs.ghtk_api.typing import FeeRequest, FeeResponse
from inno_erp.utils.address import format_location, format_ward

GRAM_CONVERSION_FACTOR = 1000  # Convert kg to grams
PROVIDERS = {"GHTK": "GHTK"}


class DeliveryOrder(BaseModel):
	service_filter: Literal["SAVING", "FAST", "EXPRESS"] = "SAVING"
	sales_order_name: str
	package_length: float
	package_width: float
	package_height: float
	package_weight: float
	package_value: float | None = None
	address_line_1: str
	address_location: str
	address_ward: str


class CalculateDeliveryFee(DeliveryOrder):
	pass


class CreateDeliveryOrder(DeliveryOrder):
	phone: str
	selected_service: str


@frappe.whitelist()
def calculate_delivery_fees(**kwargs) -> dict:
	req = CalculateDeliveryFee(**kwargs)
	order = frappe.get_doc("Sales Order", req.sales_order_name)

	branch = get_branch_by_warehouse(order.set_warehouse)

	delivery_setting = frappe.get_single("Delivery Setting")

	ghtk_token = delivery_setting.get_password("ghtk_token", raise_exception=False)

	if not delivery_setting.ghtk_enable or not ghtk_token:
		return {}

	results = []
	with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
		future_ghtk = executor.submit(get_ghtk_fee, req, branch, ghtk_token)

		results.append(future_ghtk.result(timeout=5))
	return results
	# return order


def get_ghtk_fee(req: CalculateDeliveryFee, branch: dict, token: str) -> dict:
	if req.service_filter in ["EXPRESS"]:
		return None

	client = GhtkApi(access_token=token)

	from_province, from_district = format_location(branch["custom_address_location"])
	to_province, to_district = format_location(req.address_location)

	fee_request = FeeRequest(
		pick_province=from_province,
		pick_district=from_district,
		pick_ward=format_ward(branch["custom_ward"]),
		pick_address=branch["custom_address_line"],
		address=req.address_line_1,
		province=to_province,
		district=to_district,
		ward=format_ward(req.address_ward),
		weight=req.package_weight * GRAM_CONVERSION_FACTOR,  # Convert kg to grams
		value=req.package_value or 0,  # Use 0 if value is None
	)

	if req.service_filter == "FAST":
		fee_request.deliver_option = "xteam"

	response = client.order.calculate_fee(fee_request)

	return {
		"provider": PROVIDERS["GHTK"],
		"service": response.fee.delivery_type or "Xteam",
		"fee": response.fee.fee,
	}


@frappe.whitelist()
def create_delivery_order(**kwargs):
	req = CreateDeliveryOrder(**kwargs)
	success_order = create_ghtk_order(req)

	pass


from inno_erp.libs.ghtk_api.typing import OrderInfo, OrderProduct, OrderRequest, OrderSuccess


def create_ghtk_order(req: CreateDeliveryOrder) -> OrderSuccess:
	order = frappe.get_doc("Sales Order", req.sales_order_name)

	branch = get_branch_by_warehouse(order.set_warehouse)

	delivery_setting = frappe.get_single("Delivery Setting")

	ghtk_token = delivery_setting.get_password("ghtk_token", raise_exception=False)
	client = GhtkApi(access_token=ghtk_token)

	from_province, from_district = format_location(branch["custom_address_location"])
	to_province, to_district = format_location(req.address_location)

	order_info = OrderInfo(
		id=order.name,
		pick_money=0,  # Assuming no COD for this example
		# is_freeship=1,
		pick_name=frappe.session.user,
		pick_address=branch["custom_address_line"],
		pick_ward=format_ward(branch["custom_ward"]),
		pick_district=from_district,
		pick_province=from_province,
		pick_tel=branch["custom_phone"],
		name=order.customer_name,
		address=req.address_line_1,
		province=to_province,
		district=to_district,
		ward=format_ward(req.address_ward),
		hamlet="Khác",
		tel=req.phone,
		total_weight=req.package_weight,
		value=req.package_value or 0,
	)

	if req.selected_service == "FAST":
		order_info.deliver_option = "xteam"

	products = []
	for item in order.items:
		products.append(
			OrderProduct(
				name=item.item_name,
				quantity=item.qty,
				weight=(req.package_weight / order.total_qty) * item.qty,
			)
		)

	return client.order.create_order(OrderRequest(order=order_info, products=products))


def get_branch_by_warehouse(warehouse: str) -> dict[str, str] | None:
	branch = frappe.get_all(
		"Branch",
		filters={"custom_selling_warehouse": warehouse},
		fields=[
			"name",
			"custom_address_line",
			"custom_address_location",
			"custom_ward",
			"custom_address",
			"custom_phone",
		],
	)

	if not branch:
		frappe.throw(_("No branch found for the specified warehouse: {0}").format(warehouse))

	return branch[0]
