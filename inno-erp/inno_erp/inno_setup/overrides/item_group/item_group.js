frappe.ui.form.on("Item Group", {
	item_group_name: (frm) => {
		if (frm.doc.item_group_name.includes(" ")) {
			frm.set_value("custom_abbr", frappe.get_abbr(frm.doc.item_group_name));
			return;
		}
		frm.set_value("custom_abbr", frm.doc.item_group_name);
	},
});
