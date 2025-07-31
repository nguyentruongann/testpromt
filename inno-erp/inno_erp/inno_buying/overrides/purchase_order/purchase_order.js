frappe.ui.form.on("Purchase Order", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_session(frm);
		}
	},
	refresh: (frm) => {
		if (frm.is_new()) {
			frm.set_value("schedule_date", frappe.datetime.nowdate());
		}
	},
	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Purchase Order Item", item.name);
		}
	},
});
