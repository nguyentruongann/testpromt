frappe.ui.form.on("Warehouse", {
	onload: (frm) => {
		frm.set_df_property("company", "hidden", 1);
	},
	custom_address_location: (frm) => {
		frm.set_value("custom_ward", null);
		frm.set_query("custom_ward", () => {
			return {
				filters: {
					location: frm.doc.custom_address_location,
				},
			};
		});
	},
});
