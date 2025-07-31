import frappe

# complete setup if missing
from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
from frappe.utils.data import now_datetime


def init_demo():
	frappe.clear_cache()
	if not frappe.db.a_row_exists("Company"):
		current_year = now_datetime().year
		setup_complete(
			{
				"language": "Việt",
				"country": "Vietnam",
				"timezone": "Asia/Ho_Chi_Minh",
				"currency": "VND",
				"company_name": "TadaLabs",
				"company_abbr": "T",
				"chart_of_accounts": "Standard 200 COA Vietnam",
				"fy_start_date": f"{current_year}-01-01",
				"fy_end_date": f"{current_year}-12-31",
				"setup_demo": 1,
			}
		)


def delete_ex_workspaces():
	frappe.clear_cache()
	if frappe.db.exists("Workspace", "ERPNext Integrations"):
		frappe.db.delete("Workspace", "ERPNext Integrations")
	if frappe.db.exists("Workspace", "ERPNext Settings"):
		frappe.db.delete("Workspace", "ERPNext Settings")
