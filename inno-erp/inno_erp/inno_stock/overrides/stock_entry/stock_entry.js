frappe.ui.form.on("Stock Entry", {
	onload: (frm) => {
		frm.set_df_property("custom_end_warehouse", "hidden", 1);
	},
	refresh: (frm) => {
		frm.trigger("toggle_display_warehouses");
		frm.refresh_fields("from_warehouse");
		frm.refresh_fields("to_warehouse");
	},
	stock_entry_type: (frm) => {
		const doc = frm.doc;
		const section_container = frm.fields_dict.to_warehouse.section.df.fieldname;
		frm.set_value("add_to_transit", 0);

		frm.trigger("toggle_display_warehouses");
		frm.trigger("reset_reference_warehouses");

		if (
			frm.is_new() &&
			doc.outgoing_stock_entry == null &&
			doc.stock_entry_type === "Material Transfer"
		) {
			frm.set_value("add_to_transit", 1);
			if (frm.fields_dict[section_container].collapse_link.hasClass("collapsed")) {
				frm.fields_dict[section_container].collapse();
			}
		}
	},

	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Stock Entry Detail", item.name);
		}
	},
	add_to_transit: (frm) => {
		frm.trigger("toggle_display_warehouses");
	},
	toggle_display_warehouses: (frm) => {
		const doc = frm.doc;

		if (!doc.add_to_transit) {
			frm.set_df_property("custom_end_warehouse", "hidden", 1);
			return;
		}

		if (doc.outgoing_stock_entry != null && doc.stock_entry_type === "Material Transfer") {
			frm.set_df_property("custom_end_warehouse", "hidden", 1);
		}

		if (doc.outgoing_stock_entry == null && doc.stock_entry_type === "Material Transfer") {
			frm.set_df_property("custom_end_warehouse", "hidden", 0);
		}
	},

	reset_reference_warehouses: (frm) => {
		const doc = frm.doc;

		frm.set_value("custom_end_warehouse", null);
		frm.set_value("to_warehouse", null);
		frm.set_value("from_warehouse", null);

		if (doc.stock_entry_type !== "Material Transfer") {
			frm.set_query("to_warehouse", () => {
				return {};
			});
		}

		if (doc.items && doc.items.length > 0) {
			for (let item in doc.items) {
				frappe.model.set_value(
					doc.items[item].doctype,
					doc.items[item].name,
					"s_warehouse",
					null
				);
				frappe.model.set_value(
					doc.items[item].doctype,
					doc.items[item].name,
					"t_warehouse",
					null
				);
			}
		}
	},
});
