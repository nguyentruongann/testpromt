import frappe
from frappe.core.doctype.data_import.data_import import start_import as start_import_frappe


@frappe.whitelist()
def start_import(doctype: str):
	if frappe.session.user != "Administrator":
		frappe.throw("You are not authorized to import data")

	start_import_frappe(doctype)
