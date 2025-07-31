frappe.provide("frappe.ui.form");

frappe.ui.form.Toolbar = class TadaToolbar extends frappe.ui.form.Toolbar {
	make_customize_buttons() {
		if (!frappe.boot.developer_mode) {
			return;
		}
		return super.make_customize_buttons();
	}
};
