import frappe
from erpnext.accounts.doctype.account.chart_of_accounts import (
	chart_of_accounts,
)


@frappe.whitelist()
def get_charts_for_country(country, with_standard=False):
	charts = chart_of_accounts.get_charts_for_country(country, with_standard)
	if country == "Vietnam":
		# Add the custom chart for Vietnam
		charts = ["Standard 200 COA Vietnam", *charts]

	return charts
