frappe.provide("frappe.utils");

frappe.utils.set_branch_session = (frm) => {
	frappe.utils.set_branch_cost_center(frm);
	frappe.utils.set_branch_warehouse(frm);
};

frappe.utils.set_branch_cost_center = (frm, key = "cost_center") => {
	const cost_center = frappe.defaults.get_user_default("defaults_cost_center");
	if (cost_center == null) {
		return;
	}

	if (!frm.doc[key]) {
		frm.set_value(key, frappe.defaults.get_user_default("defaults_cost_center"));
	}
};
frappe.utils.set_branch_warehouse = (frm, key = "set_warehouse") => {
	const selling_whs = frappe.defaults.get_user_default("selling_warehouse");
	if (selling_whs == null) {
		return;
	}

	if (!frm.doc[key]) {
		frm.set_value(key, selling_whs);
	}
};

frappe.utils.set_branch_cost_center_for_item = (frm, cdt, cdn, key = "cost_center") => {
	const cost_center = frappe.defaults.get_user_default("defaults_cost_center");
	if (cost_center == null) {
		return;
	}

	frappe.model.set_value(cdt, cdn, key, cost_center);
};
