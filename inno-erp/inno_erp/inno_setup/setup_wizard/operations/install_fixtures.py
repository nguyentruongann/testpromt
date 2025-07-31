# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt


import json
import os

import frappe
from erpnext import get_default_company
from erpnext.regional.address_template.setup import set_up_address_templates
from erpnext.setup.setup_wizard.operations import install_fixtures
from erpnext.setup.setup_wizard.operations.install_fixtures import (
	add_uom_data,
	read_lines,
	set_global_defaults,
	update_item_variant_settings,
)
from frappe import _
from frappe.desk.doctype.global_search_settings.global_search_settings import (
	update_global_search_doctypes,
)
from frappe.desk.page.setup_wizard.setup_wizard import make_records


def install(country=None):
	records = [
		# ensure at least an empty Address Template exists for this Country
		{"doctype": "Address Template", "country": country},
		# item group
		{
			"doctype": "Item Group",
			"item_group_name": _("All Item Groups"),
			"is_group": 1,
			"parent_item_group": "",
		},
		{
			"doctype": "Item Group",
			"item_group_name": _("Products"),
			"is_group": 0,
			"parent_item_group": _("All Item Groups"),
			"show_in_website": 1,
		},
		# Stock Entry Type
		{
			"doctype": "Stock Entry Type",
			"name": "Material Issue",
			"purpose": "Material Issue",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Material Receipt",
			"purpose": "Material Receipt",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Material Transfer",
			"purpose": "Material Transfer",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Manufacture",
			"purpose": "Manufacture",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Repack",
			"purpose": "Repack",
			"is_standard": 1,
		},
		{"doctype": "Stock Entry Type", "name": "Disassemble", "purpose": "Disassemble", "is_standard": 1},
		{
			"doctype": "Stock Entry Type",
			"name": "Send to Subcontractor",
			"purpose": "Send to Subcontractor",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Material Transfer for Manufacture",
			"purpose": "Material Transfer for Manufacture",
			"is_standard": 1,
		},
		{
			"doctype": "Stock Entry Type",
			"name": "Material Consumption for Manufacture",
			"purpose": "Material Consumption for Manufacture",
			"is_standard": 1,
		},
		# territory: with two default territories, one for home country and one named Rest of the World
		{
			"doctype": "Territory",
			"territory_name": _("All Territories"),
			"is_group": 1,
			"name": _("All Territories"),
			"parent_territory": "",
		},
		{
			"doctype": "Territory",
			"territory_name": country.replace("'", ""),
			"is_group": 0,
			"parent_territory": _("All Territories"),
		},
		{
			"doctype": "Territory",
			"territory_name": _("Rest Of The World"),
			"is_group": 0,
			"parent_territory": _("All Territories"),
		},
		# customer group
		{
			"doctype": "Customer Group",
			"customer_group_name": _("All Customer Groups"),
			"is_group": 1,
			"name": _("All Customer Groups"),
			"parent_customer_group": "",
		},
		{
			"doctype": "Customer Group",
			"customer_group_name": _("Customer"),
			"is_group": 0,
			"parent_customer_group": _("All Customer Groups"),
		},
		{
			"doctype": "Customer Group",
			"customer_group_name": _("Wholesale Customer"),
			"is_group": 0,
			"parent_customer_group": _("All Customer Groups"),
		},
		# customer
		{
			"doctype": "Customer",
			"customer_name": _("Retail Customer"),
			"customer_type": "Individual",
		},
		# supplier group
		{
			"doctype": "Supplier Group",
			"supplier_group_name": _("All Supplier Groups"),
			"is_group": 1,
			"name": _("All Supplier Groups"),
			"parent_supplier_group": "",
		},
		{
			"doctype": "Supplier Group",
			"supplier_group_name": _("Services"),
			"is_group": 0,
			"parent_supplier_group": _("All Supplier Groups"),
		},
		{
			"doctype": "Supplier Group",
			"supplier_group_name": _("Raw Material"),
			"is_group": 0,
			"parent_supplier_group": _("All Supplier Groups"),
		},
		{
			"doctype": "Supplier Group",
			"supplier_group_name": _("Distributor"),
			"is_group": 0,
			"parent_supplier_group": _("All Supplier Groups"),
		},
		# Sales Person
		{
			"doctype": "Sales Person",
			"sales_person_name": _("Sales Team"),
			"is_group": 1,
			"parent_sales_person": "",
		},
		# Mode of Payment
		{"doctype": "Mode of Payment", "mode_of_payment": _("Cash"), "type": "Cash"},
		{"doctype": "Mode of Payment", "mode_of_payment": _("Wire Transfer"), "type": "Bank"},
		# Activity Type
		{"doctype": "Activity Type", "activity_type": _("Planning")},
		{"doctype": "Activity Type", "activity_type": _("Research")},
		{"doctype": "Activity Type", "activity_type": _("Proposal Writing")},
		{"doctype": "Activity Type", "activity_type": _("Execution")},
		{"doctype": "Activity Type", "activity_type": _("Communication")},
		{
			"doctype": "Item Attribute",
			"attribute_name": _("Size"),
			"item_attribute_values": [
				{"attribute_value": _("Extra Small"), "abbr": "XS"},
				{"attribute_value": _("Small"), "abbr": "S"},
				{"attribute_value": _("Medium"), "abbr": "M"},
				{"attribute_value": _("Large"), "abbr": "L"},
				{"attribute_value": _("Extra Large"), "abbr": "XL"},
			],
		},
		{
			"doctype": "Item Attribute",
			"attribute_name": _("Colour"),
			"item_attribute_values": [
				{"attribute_value": _("Red"), "abbr": "RED"},
				{"attribute_value": _("Green"), "abbr": "GRE"},
				{"attribute_value": _("Blue"), "abbr": "BLU"},
				{"attribute_value": _("Black"), "abbr": "BLA"},
				{"attribute_value": _("White"), "abbr": "WHI"},
			],
		},
		# Issue Priority
		{"doctype": "Issue Priority", "name": _("Low")},
		{"doctype": "Issue Priority", "name": _("Medium")},
		{"doctype": "Issue Priority", "name": _("High")},
		{"doctype": "Party Type", "party_type": "Customer", "account_type": "Receivable"},
		{"doctype": "Party Type", "party_type": "Supplier", "account_type": "Payable"},
		{"doctype": "Party Type", "party_type": "Employee", "account_type": "Payable"},
		{"doctype": "Party Type", "party_type": "Shareholder", "account_type": "Payable"},
		{"doctype": "Opportunity Type", "name": _("Sales")},
		{"doctype": "Opportunity Type", "name": _("Support")},
		{"doctype": "Opportunity Type", "name": _("Maintenance")},
		{"doctype": "Project Type", "project_type": "Internal"},
		{"doctype": "Project Type", "project_type": "External"},
		{"doctype": "Project Type", "project_type": "Other"},
		{"doctype": "Print Heading", "print_heading": _("Credit Note")},
		{"doctype": "Print Heading", "print_heading": _("Debit Note")},
		# Share Management
		{"doctype": "Share Type", "title": _("Equity")},
		{"doctype": "Share Type", "title": _("Preference")},
		# Market Segments
		{"doctype": "Market Segment", "market_segment": _("Lower Income")},
		{"doctype": "Market Segment", "market_segment": _("Middle Income")},
		{"doctype": "Market Segment", "market_segment": _("Upper Income")},
		# Warehouse Type
		{"doctype": "Warehouse Type", "name": "Transit"},
		{"doctype": "Warehouse Type", "name": "Sales"},
	]

	for doctype, title_field, filename in (
		("Designation", "designation_name", "designation.txt"),
		("Sales Stage", "stage_name", "sales_stage.txt"),
		("Industry Type", "industry", "industry_type.txt"),
		("Lead Source", "source_name", "lead_source.txt"),
		("Sales Partner Type", "sales_partner_type", "sales_partner_type.txt"),
	):
		records += [{"doctype": doctype, title_field: title} for title in read_lines(filename)]

	base_path = frappe.get_app_path("erpnext", "stock", "doctype")
	response = frappe.read_file(os.path.join(base_path, "delivery_trip/dispatch_notification_template.html"))

	records += [
		{
			"doctype": "Email Template",
			"name": _("Dispatch Notification"),
			"response": response,
			"subject": _("Your order is out for delivery!"),
			"owner": frappe.session.user,
		}
	]

	# Records for the Supplier Scorecard
	from erpnext.buying.doctype.supplier_scorecard.supplier_scorecard import make_default_records

	make_default_records()
	make_records(records)
	set_up_address_templates(default_country=country)
	update_address_template_vn()
	update_vnd_currency()
	update_selling_defaults()
	update_buying_defaults()
	add_uom_data()
	update_item_variant_settings()
	update_global_search_doctypes()

	if country == "Vietnam":
		make_address_locations_vn()


install_fixtures.install = install


def update_selling_defaults():
	selling_settings = frappe.get_doc("Selling Settings")
	selling_settings.cust_master_name = "Naming Series"
	selling_settings.so_required = "No"
	selling_settings.dn_required = "No"
	selling_settings.allow_multiple_items = 1
	selling_settings.territory = "Vietnam"
	selling_settings.customer_group = _("Customer")
	selling_settings.enable_discount_accounting = 1
	selling_settings.sales_update_frequency = "Daily"
	selling_settings.save()


def update_buying_defaults():
	buying_settings = frappe.get_doc("Buying Settings")
	buying_settings.supp_master_name = "Naming Series"
	buying_settings.po_required = "No"
	buying_settings.pr_required = "No"
	buying_settings.maintain_same_rate = 1
	buying_settings.allow_multiple_items = 1
	buying_settings.save()


VIETNAM_ADDRESS_TEMPLATE = """{{ address_line1 }}<br>
{% if address_line2 %}{{ address_line2 }}<br>{% endif -%}
{% if custom_ward %}{{ custom_ward }}<br>{% endif -%}
{% if custom_address_location %}{{ custom_address_location }}<br>{% endif -%}
{{ country }}<br>
<br>
{% if phone %}{{ _("Phone") }}: {{ phone }}<br>{% endif -%}
{% if fax %}{{ _("Fax") }}: {{ fax }}<br>{% endif -%}
{% if email_id %}{{ _("Email") }}: {{ email_id }}<br>{% endif -%}
"""


def update_address_template_vn():
	address_template = frappe.get_doc("Address Template", "Vietnam")
	address_template.template = VIETNAM_ADDRESS_TEMPLATE
	address_template.save()


def update_vnd_currency():
	currency = frappe.get_doc("Currency", "VND")
	currency.symbol_on_right = True
	currency.fraction_units = 1000
	currency.smallest_currency_fraction_value = 500
	currency.save()


def install_defaults(args=None):  # nosemgrep
	records = [
		# Price Lists
		{
			"doctype": "Price List",
			"price_list_name": _("Buying"),
			"enabled": 1,
			"buying": 1,
			"selling": 0,
			"currency": args.currency,
		},
		{
			"doctype": "Price List",
			"price_list_name": _("Selling"),
			"enabled": 1,
			"buying": 0,
			"selling": 1,
			"currency": args.currency,
		},
	]

	make_records(records)

	# enable default currency
	frappe.db.set_value("Currency", args.get("currency"), "enabled", 1)
	frappe.db.set_single_value("Stock Settings", "email_footer_address", args.get("company_name"))

	set_global_defaults(args)
	update_stock_settings()

	args.update({"set_default": 1})
	create_bank_account(args)
	update_system_and_hr_settings()
	update_default_value()
	update_mode_of_payment_accounts(args)


install_fixtures.install_defaults = install_defaults

erpnext_create_bank_account = install_fixtures.create_bank_account


def update_mode_of_payment_accounts(args):
	company_name = args.get("company_name")
	if args.get("chart_of_accounts") != "Standard 200 COA Vietnam":
		return
	try:
		wire_transfer_account = frappe.db.get_value(
			"Account", {"account_number": "1121", "company": company_name}, "name"
		)
		if wire_transfer_account and frappe.db.exists("Mode of Payment", _("Wire Transfer")):
			wire_transfer_mop = frappe.get_doc("Mode of Payment", _("Wire Transfer"))
			wire_transfer_mop.accounts = []
			wire_transfer_mop.append(
				"accounts", {"company": company_name, "default_account": wire_transfer_account}
			)
			wire_transfer_mop.save()

	except Exception as e:
		frappe.log_error(f"Error updating Mode of Payment accounts: {e}")


def create_bank_account(args):
	if args.get("chart_of_accounts") != "Standard 200 COA Vietnam":
		return erpnext_create_bank_account(args)

	company_name = args.get("company_name")
	bank_account = frappe.db.get_value(
		"Account",
		{"account_type": "Bank", "root_type": "Asset", "is_group": 0, "company": company_name},
	)

	if not bank_account:
		frappe.throw(_("Can not find matched Bank Account in Chart of Accounts"))

	frappe.db.set_value(
		"Company",
		args.get("company_name"),
		"default_bank_account",
		bank_account,
		update_modified=False,
	)

	return bank_account


install_fixtures.create_bank_account = create_bank_account


def update_stock_settings():
	stock_settings = frappe.get_doc("Stock Settings")
	stock_settings.item_naming_by = "Item Code"
	stock_settings.valuation_method = "Moving Average"
	stock_settings.default_warehouse = frappe.db.get_value("Warehouse", {"warehouse_name": _("Stores")})
	stock_settings.stock_uom = _("Nos")
	stock_settings.auto_indent = 1
	stock_settings.auto_insert_price_list_rate_if_missing = 1
	stock_settings.update_price_list_based_on = "Rate"
	stock_settings.set_qty_in_transactions_based_on_serial_no_input = 1
	stock_settings.flags.ignore_permissions = True

	stock_settings.enable_stock_reservation = 1
	stock_settings.allow_partial_reservation = 0
	stock_settings.auto_reserve_stock_for_sales_order_on_purchase = 0
	stock_settings.allow_uom_with_conversion_rate_defined_in_item = 1
	stock_settings.auto_reserve_serial_and_batch = 0

	stock_settings.save()


def update_system_and_hr_settings():
	# System Settings
	system_settings = frappe.get_doc("System Settings")
	system_settings.first_day_of_the_week = "Monday"
	system_settings.number_format = "# ###.##"
	system_settings.enable_onboarding = 0
	system_settings.allow_login_using_user_name = 1
	system_settings.disable_system_update_notification = 1
	system_settings.disable_change_log_notification = 1
	system_settings.currency_precision = 2
	system_settings.allow_error_traceback = 0
	system_settings.save()

	# HR Settings
	try:
		hr_settings = frappe.get_doc("HR Settings")
		if hr_settings:
			hr_settings.allow_geolocation_tracking = True
			hr_settings.save()
	except Exception as e:
		frappe.log_error(f"Error in HR Settings: {e}")


def update_default_value():
	frappe.defaults.set_global_default("branch_master_name", "Branch Name")


def make_address_locations_vn():
	"""
	Initialize locations and wards data.
	"""
	DIR = os.path.join(os.path.dirname(__file__), "data")
	# Load locations data
	with open(DIR + "/locations.json", encoding="utf-8") as file:
		locations = json.load(file)
	location_doctype = "Address Location"
	location_fields = ["name", "province_district", "district_code", "country"]
	location_values = [
		(loc["province_district"], loc["province_district"], loc["district_code"], loc["country"])
		for loc in locations
	]
	if location_values:
		frappe.db.bulk_insert(
			doctype=location_doctype,
			fields=location_fields,
			values=location_values,
		)
	else:
		frappe.log(_("No locations data found to insert."))

	# Load wards data
	with open(DIR + "/wards.json", encoding="utf-8") as file:
		wards = json.load(file)
	ward_doctype = "Address Ward"
	ward_fields = ["name", "ward", "code", "location"]
	ward_values = [
		(f"{ward['ward']}-{ward['code']}", ward["ward"], ward["code"], ward["location"]) for ward in wards
	]

	if ward_values:
		frappe.db.bulk_insert(
			doctype=ward_doctype,
			fields=ward_fields,
			values=ward_values,
		)
	else:
		frappe.log(_("No wards data found to insert."))
