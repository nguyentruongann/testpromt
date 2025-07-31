"""
Payoo API CLI Tool

Command-line interface for testing Payoo API functionality.
Provides examples of creating, getting, and updating orders.
"""

import json
import os
from datetime import datetime, timedelta, timezone
from typing import NoReturn

from . import PayooMPOS
from .typing import CreateOrderRequest, Product

USERNAME: str = "TADALABS"
CREDENTIAL_RAW_TEXT: str = "TADALABS@123"
ACCOUNT_NAME_POS_EDC: str = "VOTCAULONGSHOP_POS"
CREATE_SHOP_CODE_POS_EDC: str = "VOTCAULONGSHOP_POS01"

# Order status constants (assuming these values from C#)
ORDERSTATUS_WAITING_FOR_PAYMENT: int = 1
ORDERSTATUS_ORDER_PAID: int = 2

ORDER_LINK_NOTIFY: str = (
	"https://f59339d78768.ngrok-free.app"  # const string ORDER_LINK_NOTIFY = "https://partner.com/notify";
)


def main() -> NoReturn:
	"""
	Main menu function - match với C# Main(string[] args)
	"""
	try:
		api = ""
		while api != "0":
			print("1: Create Order on PAYOO EDC:")
			print("2: Query Order")
			print("3: Cancel Order (unpaid)")
			print("Please choose:", end="")
			api = input().strip()

			if api == "1":
				create_pos_order()
			elif api == "2":
				get_order()
			elif api == "3":
				cancel_order()
			else:
				pass

			os.system("clear" if os.name == "posix" else "cls")

	except Exception as ex:
		print(f"Exception:{ex}")


def cancel_order():
	"""Cancel Order - match với C# CancelOrder function"""
	payoo = PayooMPOS(
		username=USERNAME,
		account_name=ACCOUNT_NAME_POS_EDC,
		credential_plain=CREDENTIAL_RAW_TEXT,
		private_key_path="/workspace/development/Key/PrivateKey_Of_Partner.pem",
		payoo_public_key_path="/workspace/development/Key/PublicKey_Of_Payoo.pem",
	)

	print("Order code:", end="")
	order_code = input().strip()

	try:
		# Sử dụng PayooOrderAPI thông qua payoo.order
		response = payoo.order.cancel(order_code)

		# Convert response model thành dict để print
		response_dict = response.model_dump()
		print(f"Response from Payoo: {json.dumps(response_dict, separators=(',', ':'))}")

	except Exception as e:
		print(f"Exception occurred: {e}")
		input()
		return

	if response.ReturnCode != 0:
		print(f"Update cancel order (unpaid) error. Error:{response.ReturnCode}, Desc:{response.Description}")
		input()
		return

	print(f"Update cancel order (unpaid) {order_code} successfully")
	input()


def create_pos_order():
	"""Create POS Order - match với C# Create_POS_Order function"""
	payoo = PayooMPOS(
		username=USERNAME,
		account_name=ACCOUNT_NAME_POS_EDC,
		credential_plain=CREDENTIAL_RAW_TEXT,
		private_key_path="/workspace/development/Key/PrivateKey_Of_Partner.pem",
		payoo_public_key_path="/workspace/development/Key/PublicKey_Of_Payoo.pem",
	)

	print("Order code:", end="")
	order_code = input().strip()

	product1 = Product(
		Name="Xiaomi Mi Band 5",
		SKU="SKU12345",
		MoneyAmount=12270000,
		Quantity=1,
		TotalAmountWithoutVAT=12270000,
		VATPercent=10,
		VATAmount=1227000,
		TotalAmountWithVAT=13497000,
	)

	product2 = Product(
		Name="Xiaomi Mi Band 6",
		SKU="SKU67890",
		MoneyAmount=15000000,
		Quantity=1,
		TotalAmountWithoutVAT=15000000,
		VATPercent=10,
		VATAmount=1500000,
		TotalAmountWithVAT=16500000,
	)
	order_amount = product1.TotalAmountWithVAT + product2.TotalAmountWithVAT
	extra_minutes = 15
	utc_plus_7 = timezone(timedelta(hours=7))  # UTC+7 timezone
	order_expired_date = (datetime.now(utc_plus_7) + timedelta(minutes=extra_minutes)).strftime(
		"%Y%m%d%H%M%S"
	)

	create_req = CreateOrderRequest(
		AccountName=ACCOUNT_NAME_POS_EDC,
		OrderCode=order_code,
		OrderAmount=order_amount,
		OrderExpiredDate=order_expired_date,
		CreateShopCode=CREATE_SHOP_CODE_POS_EDC,
		OrderLinkNotify=ORDER_LINK_NOTIFY,
		CustomerCode="XMC001",
		CustomerName="THOMAS",
		CustomerAddress="35 NGUYEN HUE STREET, DIST 1",
		CustomerPhone="0989999999",
		CustomerEmail="thomas@gmail.com",
		OrderNote="some simple note for order here",
		TerminalID="ID of partner device",
		PartnerShopCode="The identification of partner store",
		PartnerInfoEx="The extra information of partner",
		Products=[product1, product2],
	)
	try:
		# Sử dụng PayooOrderAPI thông qua payoo.order
		response = payoo.order.create(create_req)

		# Convert response model thành dict để print
		response_dict = response.model_dump()
		print(f"Response from Payoo: {json.dumps(response_dict, separators=(',', ':'))}")

	except Exception as e:
		print(f"Exception occurred: {e}")
		input()
		return

	print(f"Create POS order {order_code} successfully")
	input()


def get_order():
	"""Get Order - match với C# GetOrder function"""
	payoo = PayooMPOS(
		username=USERNAME,
		account_name=ACCOUNT_NAME_POS_EDC,
		credential_plain=CREDENTIAL_RAW_TEXT,
		private_key_path="/workspace/development/Key/PrivateKey_Of_Partner.pem",
		payoo_public_key_path="/workspace/development/Key/PublicKey_Of_Payoo.pem",
	)

	print("Order code:", end="")
	order_code = input().strip()

	try:
		# Sử dụng PayooOrderAPI thông qua payoo.order
		response = payoo.order.get(order_code)

		# Convert response model thành dict để print
		response_dict = response.model_dump()
		print(f"Response from Payoo: {json.dumps(response_dict, separators=(',', ':'))}")

	except Exception as e:
		print(f"Exception occurred: {e}")
		input()
		return

	if response.ReturnCode == -33:
		print(f"Order {order_code} does not exist in the Payoo system.")
		input()
		return

	if response.ReturnCode != 0:
		print(f"Error retrieving order information. Error:{response.ReturnCode}, Desc:{response.Description}")
		input()
		return

	print("Order information retrieved successfully")

	if response.ResponseData is not None:
		get_res = response.ResponseData
		print("------ORDER INFORMATION------")
		print("Order code:" + str(get_res.OrderCode))
		print("Amount:" + str(get_res.OrderAmount))
		print("Status:" + str(get_res.Status))
		print("Order expire date:" + str(get_res.OrderExpireDate))
		print("Order note:" + str(get_res.OrderNote or ""))
		print("Customer name:" + str(get_res.CustomerName or ""))
		print("Customer address:" + str(get_res.CustomerAddress or ""))
		print("Customer phone:" + str(get_res.CustomerPhone or ""))
		print("Customer email:" + str(get_res.CustomerEmail or ""))
		print("Create date:" + str(get_res.CreateDate))

		if get_res.Status == ORDERSTATUS_WAITING_FOR_PAYMENT:
			print("The order is waiting for payment.")

		if get_res.Status == ORDERSTATUS_ORDER_PAID:
			print("The order has been paid successfully.")

	input()


if __name__ == "__main__":
	main()
