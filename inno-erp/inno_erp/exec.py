import frappe

# complete setup if missing
from frappe.desk.page.setup_wizard.setup_wizard import setup_complete
from frappe.utils.data import now_datetime

LANG = "Việt"  # Việt - en


def init_inno():
	frappe.clear_cache()
	# Initialize company if missing
	if not frappe.db.a_row_exists("Company"):
		current_year = now_datetime().year
		setup_complete(
			{
				"language": LANG,
				"country": "Vietnam",
				"timezone": "Asia/Ho_Chi_Minh",
				"currency": "VND",
				"company_name": "Tadalabs",
				"company_abbr": "TL",
				"chart_of_accounts": "Standard 200 COA Vietnam",
				"fy_start_date": f"{current_year}-01-01",
				"fy_end_date": f"{current_year}-12-31",
				"setup_demo": 0,
			}
		)


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
				"company_name": "Tadalabs",
				"company_abbr": "TL",
				"chart_of_accounts": "Standard 200 COA Vietnam",
				"fy_start_date": f"{current_year}-01-01",
				"fy_end_date": f"{current_year}-12-31",
				"setup_demo": 1,
			}
		)
