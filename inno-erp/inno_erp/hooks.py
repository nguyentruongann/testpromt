app_name = "inno_erp"
app_title = "InnoERP"
app_publisher = "Tada Labs"
app_description = "InnoERP"
app_email = "info@tadalabs.vn"
app_license = "gpl-3.0"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "inno_erp",
# 		"logo": "/assets/inno_erp/logo.png",
# 		"title": "InnoERP",
# 		"route": "/inno_erp",
# 		"has_permission": "inno_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "inno.bundle.css"
app_include_js = "inno.bundle.js"

# include js, css files in header of web template
# web_include_css = "/assets/inno_erp/css/inno_erp.css"
# web_include_js = "/assets/inno_erp/js/inno_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "inno_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
page_js = {
	# Stock
	"print": "inno_stock/page/print/print.js",
	# Selling
	"point-of-sale": "inno_selling/page/point_of_sale/point_of_sale.js",
}

# include js in doctype views
doctype_js = {
	# Setup
	"Company": "inno_setup/overrides/company/company.js",
	"Address": "inno_setup/overrides/address/address.js",
	"Brand": "inno_setup/overrides/brand/brand.js",
	"Branch": "inno_setup/overrides/branch/branch.js",
	"Item Group": "inno_setup/overrides/item_group/item_group.js",
	# Stock
	"Item": [
		"inno_stock/overrides/item/item_combo_items.js",
		"inno_stock/overrides/item/item_variant_details.js",
		"inno_stock/overrides/item/item_dialog.js",
		"inno_stock/overrides/item/item.js",
	],
	"Warehouse": "inno_stock/overrides/warehouse/warehouse.js",
	"Stock Entry": "inno_stock/overrides/stock_entry/stock_entry.js",
	"Stock Reconciliation": "inno_stock/overrides/stock_reconciliation/stock_reconciliation.js",
	"Material Request": "inno_stock/overrides/material_request/material_request.js",
	"Purchase Receipt": "inno_stock/overrides/purchase_receipt/purchase_receipt.js",
	"Delivery Note": "inno_stock/overrides/delivery_note/delivery_note.js",
	# Core
	"User": "inno_core/overrides/user/user.js",
	# Account
	"Sales Invoice": [
		"inno_account/overrides/sales_invoice/sales_invoice_payment.js",
		"inno_account/overrides/sales_invoice/sales_invoice_print.js",
		"inno_account/overrides/sales_invoice/sales_invoice.js",
	],
	"Purchase Invoice": "inno_account/overrides/purchase_invoice/purchase_invoice.js",
	"Loyalty Program": "inno_account/overrides/loyalty_program/loyalty_program.js",
	"POS Invoice": "inno_account/overrides/pos_invoice/pos_invoice.js",
	# Selling
	"Sales Order": [
		"inno_selling/overrides/sales_order/sales_order.js",
		"inno_selling/overrides/sales_order/sales_order_delivery.js",
	],
	# Buying
	"Purchase Order": "inno_buying/overrides/purchase_order/purchase_order.js",
	# Product Bundle
	"Product Bundle": "inno_selling/overrides/product_bundle/product_bundle.js",
	# Coupon Code
	"Coupon Code": "inno_account/overrides/coupon_code/coupon_code.js",
}
doctype_list_js = {
	# Stock
	"Item": "inno_stock/overrides/item/item_list.js",
	"Branch": "inno_setup/overrides/branch/branch_list.js",
	"Item Price": "inno_stock/overrides/item_price/item_price_list.js",
}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "inno_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "inno_erp.utils.jinja_methods",
# 	"filters": "inno_erp.utils.jinja_filters"
# }

# Installation
# ------------

before_install = "inno_erp.inno_setup.install.before_install"
after_install = "inno_erp.inno_setup.install.after_install"
after_migrate = "inno_erp.inno_setup.install.after_migrate"

# Fixtures
# --------
# Automatically install these fixtures during app setup
# fixtures = [
# 	{"doctype": "Ecommerce Platform", "filters": {"platform_code": ["in", ["lazada", "shopee", "tiktok"]]}}
# ]

# Uninstallation
# ------------

# before_uninstall = "inno_erp.uninstall.before_uninstall"
# after_uninstall = "inno_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "inno_erp.utils.before_app_install"
# after_app_install = "inno_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "inno_erp.utils.before_app_uninstall"
# after_app_uninstall = "inno_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "inno_erp.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	# Account
	# Setup
	"Company": "inno_erp.inno_setup.overrides.company.company.InnoCompany",
	"Brand": "inno_erp.inno_setup.overrides.brand.brand.InnoBrand",
	"Branch": "inno_erp.inno_setup.overrides.branch.branch.InnoBranch",
	"Item Group": "inno_erp.inno_setup.overrides.item_group.item_group.InnoItemGroup",
	# Stock
	"Item": "inno_erp.inno_stock.overrides.item.item.InnoItem",
	"Stock Reconciliation": "inno_erp.inno_stock.overrides.stock_reconciliation.stock_reconciliation.InnoStockReconciliation",
	# Selling
	"Customer": "inno_erp.inno_selling.overrides.customer.customer.InnoCustomer",
	# Account
	"POS Invoice": "inno_erp.inno_account.overrides.pos_invoice.pos_invoice.InnoPOSInvoice",
	"Sales Invoice": "inno_erp.inno_account.overrides.sales_invoice.sales_invoice.InnoSalesInvoice",
	"Product Bundle": "inno_erp.inno_selling.overrides.product_bundle.product_bundle.InnoProductBundle",
	"Coupon Code": "inno_erp.inno_account.overrides.coupon_code.coupon_code.InnoCouponCode",
}

# Document Events
# ---------------
# Hook on document methods and events
ECOM_INDEXES = [
	"Item",
	"Omni Item",
	"Pricing Rule",
	"Stock Reservation Entry",
	"Stock Ledger Entry",
	"POS Invoice",
	"Item Price",
]

doc_events = {
	tuple(ECOM_INDEXES): {
		"on_change": "inno_erp.search.ecom_index.on_change",
		"on_trash": "inno_erp.search.ecom_index.on_change",
	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
	# 	"inno_erp.tasks.all"
	# ],
	"daily": [
		"inno_erp.inno_account.doctype.loyalty_setting.loyalty_setting.reset_loyalty_points",
	],
	# "hourly": [
	# 	"inno_erp.tasks.hourly"
	# ],
	# "weekly": [
	# 	"inno_erp.tasks.weekly"
	# ],
	# "monthly": [
	#     "inno_erp.inno_account.overrides.customer.customer.reset_customer_loyalty_points",
	# ],
}

# Testing
# -------

# before_tests = "inno_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts.get_charts_for_country": "inno_erp.inno_account.overrides.account.chart_of_accounts.chart_of_accounts.get_charts_for_country",
	"frappe.core.doctype.session_default_settings.session_default_settings.get_session_default_values": "inno_erp.inno_core.overrides.session_default_settings.session_default_settings.get_session_default_values",
	"frappe.core.doctype.session_default_settings.session_default_settings.set_session_default_values": "inno_erp.inno_core.overrides.session_default_settings.session_default_settings.set_session_default_values",
	"erpnext.stock.doctype.stock_entry.stock_entry.make_stock_in_entry": "inno_erp.inno_stock.overrides.stock_entry.stock_entry.make_stock_in_entry",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps


# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["inno_erp.utils.before_request"]
# after_request = ["inno_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["inno_erp.utils.before_job"]
# after_job = ["inno_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"inno_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
export_python_type_annotations = True

website_route_rules = [
	{"from_route": "/hrms/<path:app_path>", "to_route": "hrms"},
]


# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
