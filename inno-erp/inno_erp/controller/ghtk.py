import frappe


@frappe.whitelist(allow_guest=True)
def webhook(**kwargs):
	print(kwargs)
	frappe.log_error("GHTK Webhook", frappe.as_json(kwargs))
	return {"message": "OK"}
