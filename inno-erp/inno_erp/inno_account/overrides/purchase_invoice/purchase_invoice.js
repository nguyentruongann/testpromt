frappe.ui.form.on("Purchase Invoice", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_cost_center(frm);
		}
	},
	refresh: (frm) => {
		if (frm.is_new()) {
			frm.set_value("due_date", frappe.datetime.nowdate());
		}
	},
	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Purchase Invoice Item", item.name);
		}
	}
});
