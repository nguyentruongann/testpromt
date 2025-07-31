frappe.ui.form.on("Branch", {
	refresh: (frm) => {
		frm.set_value("custom_company", frappe.defaults.get_user_default("Company"));
		frm.set_df_property("custom_company", "hidden", 1);
		frm.set_df_property("custom_naming_series", "hidden", 1);
	},
	custom_address_location: (frm) => {
		frm.set_query("custom_ward", () => {
			return {
				filters: {
					location: frm.doc.custom_address_location,
				},
			};
		});
		frm.set_value("custom_ward", "");
	},
});
