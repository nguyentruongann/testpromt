// Copyright (c) 2025, TadaLabs and contributors
// For license information, please see license.txt

frappe.ui.form.on("Address", {
	refresh(frm) {
		if (frm.doc.country === "Vietnam") {
			frm.set_df_property("city", "hidden", 1);
			frm.set_df_property("county", "hidden", 1);
			frm.set_df_property("state", "hidden", 1);

			frm.set_df_property("custom_address_location", "read_only", 0);

			if (frm.doc.custom_address_location) {
				frm.set_df_property("custom_ward", "read_only", 0);
			} else {
				frm.set_df_property("custom_ward", "read_only", 1);
			}
		} else {
			frm.set_df_property("custom_address_location", "hidden", 1);
			frm.set_df_property("custom_ward", "hidden", 1);
			frm.set_df_property("city", "hidden", 0);
			frm.set_df_property("county", "hidden", 0);
			frm.set_df_property("state", "hidden", 0);
		}
	},
	custom_address_location(frm, cdt, cdn) {
		frm.set_value("city", frm.doc.custom_address_location);
		if (frm.doc.custom_address_location) {
			frm.set_df_property("custom_ward", "read_only", 0);
			frm.set_query("custom_ward", () => {
				return {
					filters: {
						location: frm.doc.custom_address_location,
					},
				};
			});
		} else {
			frm.set_df_property("custom_ward", "read_only", 1);
		}
	},
});
