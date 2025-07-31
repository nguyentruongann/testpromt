import frappe
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import make_closing_entry_from_opening
from frappe import _

# Handle dynamic schedule time by using:
# https://docs.frappe.io/framework/user/en/api/background_jobs


def auto_close_pos_sessions():
	open_entries = frappe.db.get_all(
		"POS Opening Entry",
		filters={"pos_closing_entry": ["in", ["", None]], "docstatus": 1},
		fields=["name", "company", "pos_profile", "period_start_date"],
		order_by="period_start_date desc",
	)

	if not open_entries:
		return

	for entry in open_entries:
		try:
			opening_doc = frappe.get_doc("POS Opening Entry", entry.name)
			make_closing_entry_from_opening(opening_doc).insert(ignore_permissions=True)
			frappe.db.commit()
			frappe.db.clear_cache()
		except Exception:
			frappe.db.rollback()
	return "All POS Sessions were closed"


@frappe.whitelist(methods="POST")
def create_pos_closing_entry(pos_profile_name):
	open_vouchers = frappe.db.get_all(
		"POS Opening Entry",
		filters={"pos_profile": pos_profile_name, "pos_closing_entry": ["in", ["", None]], "docstatus": 1},
		fields=["name"],
		order_by="period_start_date desc",
		limit_page_length=1,
	)

	if not open_vouchers:
		frappe.throw(_("No opening entry found for pos profile {0}").format(pos_profile_name))

	opening_doc = frappe.get_doc("POS Opening Entry", open_vouchers[0].name)

	closing_doc = make_closing_entry_from_opening(opening_doc).insert(ignore_permissions=True)
	frappe.db.commit()
	return closing_doc.name
