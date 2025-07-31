frappe.ui.form.on("Material Request", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_warehouse(frm);
		}
	},
	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Material Request Item", item.name);
		}
	},
});
