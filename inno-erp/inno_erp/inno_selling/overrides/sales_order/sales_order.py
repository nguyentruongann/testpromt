import frappe
from erpnext.selling.doctype.sales_order import sales_order
from erpnext.selling.doctype.sales_order.sales_order import (
	make_sales_invoice as erp_make_sales_invoice,
)


@frappe.whitelist()
def inno_make_sales_invoice(source_name, target_doc=None, ignore_permissions=False):
	doclist = erp_make_sales_invoice(source_name, target_doc, ignore_permissions)

	source = frappe.get_doc("Sales Order", source_name)

	if source.get("custom_redeem_loyalty_points"):
		doclist.redeem_loyalty_points = 1
		doclist.loyalty_points = source.loyalty_points
		doclist.loyalty_amount = source.loyalty_amount
		doclist.loyalty_program = source.get("custom_loyalty_program")

	if source.get("coupon_code"):
		doclist.custom_coupon_code = source.coupon_code

	for field in doclist.meta.fields:
		if field.fieldname == "custom_select_pricing_rule":
			field.hidden = 1
			break

	return doclist


sales_order.make_sales_invoice = inno_make_sales_invoice
