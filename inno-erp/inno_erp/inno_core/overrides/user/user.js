frappe.ui.form.on("User", {
	refresh(frm) {
		// hide language if is not dev env
		if (!frappe.boot.developer_mode) {
			frm.set_df_property("language", "hidden", 1);
		}
	},
});
