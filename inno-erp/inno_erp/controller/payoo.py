import frappe
from frappe import _
from frappe.utils import add_days, cint, flt, getdate, now_datetime

from inno_erp.libs.payoo_api import PayooMPOS
from inno_erp.libs.payoo_api.typing import *

VIETQR_PATTERN = (
	"https://img.vietqr.io/image/{bank_swift}-{bank_account_no}-compact2.png?amount={amount}&addInfo={title}"
)


@frappe.whitelist()
def get_bank_qr_code_url(sales_invoice_name):
	sales_invoice = frappe.db.get_value(
		"Sales Invoice", sales_invoice_name, ["outstanding_amount"], as_dict=True
	)

	if not sales_invoice or sales_invoice.outstanding_amount <= 0:
		frappe.throw(_("Sales Invoice not found or has no outstanding amount"))

	bank_account = frappe.db.get_value(
		"Bank Account", {"is_default": 1}, ["bank", "bank_account_no"], as_dict=True
	)

	if not bank_account:
		frappe.throw(_("Bank Account not found"))

	bank = frappe.get_doc("Bank", bank_account.bank)

	title = f"Thanh toán hóa đơn {sales_invoice_name}"
	url = VIETQR_PATTERN.format(
		bank_swift=bank.swift_number,
		bank_account_no=bank_account.bank_account_no,
		amount=sales_invoice.outstanding_amount,
		title=title,
	)
	return url


@frappe.whitelist()
def create_payment_request(sales_invoice_name, payment_method):
	payment_setting = frappe.get_single("Payment Setting")
	payoo_mpos = get_payoo_client()

	sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)
	# payoo_orders = frappe.get_all(
	# 	"Payoo Order",
	# 	filters={"parent": sales_invoice_name},
	# 	fields=["name", "status_code", "payment_method", "expired_date"],
	# )
	payment_methods = {"0": "PHYSICAL CARD", "2": "QR CODE"}

	new_payoo_order = frappe.get_doc(
		{
			"doctype": "Payoo Order",
			"parent": sales_invoice_name,
			"parenttype": "Sales Invoice",
			"parentfield": "custom_payoo_orders",
			"status_code": 0,
			"payment_method": payment_methods[payment_method],
			"expired_date": add_days(now_datetime(), 7),
		}
	)
	new_payoo_order.insert()

	list_products = []

	for item in sales_invoice.items:
		product = Product(
			Name=item.get("item_name", ""),
			SKU=item.get("item_code", ""),
			MoneyAmount=flt(item.get("rate", 0)) * flt(item.get("qty", 0)),
			Size="",
			Quantity=cint(item.get("qty", 0)),
			Unit=item.get("uom", None),
			TotalAmountWithoutVAT=flt(item.get("base_net_amount", 0)),
			VATPercent=cint(item.get("tax_rate", 0)),
			VATAmount=flt(item.get("tax_amount", 0)),
			TotalAmountWithVAT=flt(item.get("base_total", 0)),
		)
		list_products.append(product)

	create_order_request = CreateOrderRequest(
		OrderCode=new_payoo_order.name,
		OrderAmount=flt(sales_invoice.outstanding_amount),
		OrderExpiredDate=add_days(getdate(), 1).strftime("%Y%m%d%H%M%S"),
		AccountName=payment_setting.payoo_account_name,
		CreateShopCode=payment_setting.payoo_create_shop_code,
		CustomerName=sales_invoice.customer_name,
		Products=list_products,
		PaymentMethod=payment_methods[payment_method],
		# OrderLinkNotify=payment_setting.payoo_order_link_notify,
		OrderLinkNotify=frappe.utils.get_url(
			f"/api/method/inno_erp.controller.payoo.order_notify?order={new_payoo_order.name}"
		),
		# OrderLinkNotify=f"https://e79799483ea9.ngrok-free.app/api/method/inno_erp.controller.payoo.order_notify?order={new_payoo_order.name}",
	)
	print(create_order_request.model_dump())
	order = payoo_mpos.order.create(create_order_request)
	print(order.model_dump())

	# if payoo_orders:
	# 	for order in payoo_orders:
	# 		if (
	# 			order.status_code == 0
	# 			and order.payment_method == payment_methods[payment_method]
	# 			and now_datetime() <= order.expired_date
	# 		):
	# 			return get_payoo_order(order.name)
	# 		frappe.db.set_value("Payoo Order", order.name, "status_code", 2)

	# new_payoo_order.order_name = new_payoo_order.name
	# new_payoo_order.save()

	return order.ResponseData.model_dump()


def get_payoo_client():
	payment_setting = frappe.get_single("Payment Setting")
	file_private = frappe.get_doc("File", {"file_url": payment_setting.payoo_private_key_path})
	full_path_private = file_private.get_full_path()
	file_public = frappe.get_doc("File", {"file_url": payment_setting.payoo_public_key_path})
	full_path_public = file_public.get_full_path()
	return PayooMPOS(
		username=payment_setting.payoo_username,
		account_name=payment_setting.payoo_account_name,
		credential_plain=payment_setting.get_password("payoo_credential_plain"),
		private_key_path=full_path_private,
		payoo_public_key_path=full_path_public,
	)


@frappe.whitelist()
def get_payoo_order(order_code):
	payoo_mpos = get_payoo_client()
	order = payoo_mpos.order.get(order_code)
	return order.ResponseData.__dict__


@frappe.whitelist()
def cancel_payoo_order(order_code):
	payoo_mpos = get_payoo_client()
	order = payoo_mpos.order.cancel(order_code)
	return order.ResponseData.__dict__


class OrderNotifyRequest(BaseModel):
	"""
	Định nghĩa mô hình dữ liệu cho yêu cầu thông báo đơn hàng.
	"""

	OrderNo: str
	PaymentStatus: int
	OrderAmount: int
	VoucherAmount: int | None = None
	PaymentAmount: int | None = None
	PaymentMethod: int | None = None
	CardNumber: str | None = None
	Period: int | None = None


@frappe.whitelist(methods=["POST"], allow_guest=True)
def order_notify(**kwargs):
	print(kwargs)
	req = OrderNotifyRequest(**kwargs)
	print("Order notify")
	return 1


@frappe.whitelist()
def submit_sales_invoice(sales_invoice_name, mode_of_payment, payment_method, amount):
	sales_invoice = frappe.get_doc("Sales Invoice", sales_invoice_name)

	if sales_invoice.docstatus == 1:
		frappe.throw(_("Sales Invoice {0} is already submitted.").format(sales_invoice_name))

	if mode_of_payment == _("Payoo"):
		payoo_orders = frappe.db.get_value(
			"Payoo Order",
			{
				"parent": sales_invoice.name,
				"status_code": 0,
				"payment_method": payment_method,
				"expired_date": [">", now_datetime()],
			},
			"name",
		)
		if not payoo_orders:
			return {"success": 0, "message": _("No Payoo order found for this sales invoice.")}
	sales_invoice.submit()

	pe = frappe.new_doc("Payment Entry")
	pe.payment_type = "Receive"
	pe.company = sales_invoice.company
	pe.reference_no = sales_invoice.name
	pe.reference_type = "Sales Invoice"
	pe.reference_date = sales_invoice.posting_date
	pe.party_type = "Customer"
	pe.party = sales_invoice.customer
	pe.posting_date = sales_invoice.posting_date
	pe.paid_from = frappe.db.get_value("Account", {"account_number": "131"}, "name")
	if mode_of_payment == _("Cash"):
		pe.paid_to = frappe.db.get_value("Account", {"account_number": "1111"}, "name")
	else:
		pe.paid_to = frappe.db.get_value("Account", {"account_number": "1121"}, "name")
	# pe.paid_from_account_currency = party_currency if payment_type == "Receive" else bank_currency
	# pe.paid_to_account_currency = party_currency if payment_type == "Pay" else bank_currency
	pe.paid_amount = flt(amount)
	pe.received_amount = flt(amount)
	pe.mode_of_payment = mode_of_payment
	# pe.project = project
	# pe.cost_center = cost_center
	pe.append(
		"references",
		{
			"reference_doctype": "Sales Invoice",
			"reference_name": sales_invoice.name,
			"allocated_amount": flt(amount),
		},
	)
	pe.validate()
	pe.insert()
	pe.submit()
	frappe.db.set_value(
		"Payoo Order",
		{
			"status_code": 0,
			"payment_method": payment_method,
			"parent": sales_invoice.name,
			"expired_date": [">", now_datetime()],
		},
		"status_code",
		1,
	)
	frappe.db.set_value(
		"Payoo Order", {"parent": sales_invoice.name, "status_code": ["!=", 1]}, "status_code", 2
	)
	return {"success": 1, "message": _("Payment submitted successfully.")}
