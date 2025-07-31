import json

import frappe
from frappe import _


@frappe.whitelist()
def get_session_default_values():
	settings = frappe.get_single("Session Default Settings")
	fields = []

	company_count = frappe.db.count("Company")
	default_company = frappe.defaults.get_user_default("company") if company_count == 1 else None

	for default_values in settings.session_defaults:
		reference_doctype = frappe.scrub(default_values.ref_doctype)

		if default_values.ref_doctype == "Company" and company_count == 1 and default_company:
			fields.append(
				{
					"fieldname": reference_doctype,
					"fieldtype": "Link",
					"label": _("Default {0}").format(_(default_values.ref_doctype)),
					"default": default_company,
					"hidden": 1,
				}
			)
		else:
			fields.append(
				{
					"fieldname": reference_doctype,
					"fieldtype": "Link",
					"options": default_values.ref_doctype,
					"label": _("Default {0}").format(_(default_values.ref_doctype)),
					"default": frappe.defaults.get_user_default(reference_doctype),
				}
			)

	return json.dumps(fields)


@frappe.whitelist()
def set_session_default_values(default_values):
	try:
		default_values = frappe.parse_json(default_values)

		if not isinstance(default_values, dict):
			frappe.throw(_("default_values must be a dictionary"))

		branch = default_values.get("branch")
		if branch:
			branch_doc = frappe.get_doc("Branch", branch)

			cost_center = branch_doc.get("custom_cost_center")
			default_warehouse = branch_doc.get("custom_warehouse")
			selling_warehouse = branch_doc.get("custom_selling_warehouse")

			if cost_center:
				default_values["defaults_cost_center"] = cost_center
			if default_warehouse:
				default_values["default_warehouse"] = default_warehouse
			if selling_warehouse:
				default_values["selling_warehouse"] = selling_warehouse

		for entry in default_values:
			try:
				frappe.defaults.set_user_default(entry, default_values.get(entry))
			except Exception as e:
				frappe.log_error(
					"Error while saving Session Default",
					f"Error while saving Session Default {entry}: {e!s}",
				)
				continue

		return "success"

	except Exception as e:
		frappe.log_error(
			"Error while saving Session Defaults",
			f"Error while saving Session Defaults: {e!s}",
		)
		return {"error": str(e)}
