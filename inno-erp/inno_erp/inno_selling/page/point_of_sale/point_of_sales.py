import frappe

POS_PROFILE_TEMPLATE = "{branch} - POS"


@frappe.whitelist()
def check_opening_entry(branch):
	open_vouchers = frappe.db.get_all(
		"POS Opening Entry",
		filters={
			"pos_profile": POS_PROFILE_TEMPLATE.format(branch=branch),
			"pos_closing_entry": ["in", ["", None]],
			"docstatus": 1,
		},
		fields=["name", "company", "pos_profile", "period_start_date"],
		order_by="period_start_date desc",
	)

	return open_vouchers
