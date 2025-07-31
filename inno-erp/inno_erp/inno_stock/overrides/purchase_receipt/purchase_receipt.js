frappe.ui.form.on("Purchase Receipt", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_session(frm);
		}
	},
	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Purchase Receipt Item", item.name);
		}
	}
});
