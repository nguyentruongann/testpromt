import frappe


# TODO: Should be handled on settings
def setup_multi_branch():
	add_branch_to_session_defaults()


def add_branch_to_session_defaults():
	settings = frappe.get_single("Session Default Settings")
	settings.append("session_defaults", {"ref_doctype": "Branch"})
	settings.save()


def before_install():
	clear_erpnext_workspaces()
	init_inno_settings()


def init_inno_settings():
	DEFAULT_LOGO = "/assets/inno_erp/images/tada-logo.png"
	DEFAULT_ICON = "/assets/inno_erp/images/tada-icon.png"
	DEFAULT_APP_NAME = "Inno ERP"

	# Navbar Settings
	navbar_settings = frappe.get_doc("Navbar Settings")
	navbar_settings.app_logo = DEFAULT_LOGO
	navbar_settings.save()

	# Website Settings
	website_settings = frappe.get_doc("Website Settings")
	website_settings.home_page = "/app"
	website_settings.app_name = DEFAULT_APP_NAME
	website_settings.title_prefix = DEFAULT_APP_NAME
	website_settings.favicon = DEFAULT_ICON
	website_settings.app_logo = DEFAULT_LOGO
	website_settings.banner_image = DEFAULT_LOGO
	website_settings.splash_image = DEFAULT_LOGO
	website_settings.footer_logo = DEFAULT_LOGO
	website_settings.footer_powered = DEFAULT_APP_NAME
	website_settings.copyright = DEFAULT_APP_NAME
	website_settings.save()


def after_install():
	remove_unused_navbar_items()


def remove_unused_navbar_items():
	NAVBAR_ITEMS_TO_REMOVE = ["My Profile", "Apps", "Toggle Full Width", "Toggle Theme", "View Website"]
	items_to_remove = frappe.db.get_list(
		"Navbar Item", filters={"item_label": ("in", NAVBAR_ITEMS_TO_REMOVE)}
	)
	for item in items_to_remove:
		frappe.db.delete("Navbar Item", item.name)


def after_migrate():
	clear_erpnext_workspaces()


# TODO: Should read all modules of workspaces from Inno Setup
def clear_erpnext_workspaces():
	frappe.clear_cache()
	workspaces = frappe.get_all(
		"Workspace",
		filters=[
			["module", "not like", "Inno%"],
		],
		or_filters=[
			["name", "!=", "Welcome Workspace"],
		],
		limit=1000,
		pluck="name",
	)
	frappe.db.delete("Workspace", {"name": ("in", workspaces)})
	frappe.db.commit()


def project_before_migrate(module):
	frappe.clear_cache()
	workspaces = frappe.get_all(
		"Workspace",
		filters=[
			["module", "!=", module],
		],
		or_filters=[
			["name", "!=", "Welcome Workspace"],
		],
		limit=1000,
		pluck="name",
	)
	frappe.db.delete("Workspace", {"name": ("in", workspaces)})
	frappe.db.commit()
