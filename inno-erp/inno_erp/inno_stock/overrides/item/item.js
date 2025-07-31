frappe.provide("inno_erp.item");
frappe.ui.form.on("Item", {
	refresh: (frm) => {
		if (frm.doc.custom_is_combo) {
			frm.set_df_property("has_variants", "hidden", 1);
			frm.set_df_property("custom_combo_items_html", "hidden", 0);
			frm.set_value("has_variants", 0);
		} else {
			frm.set_df_property("has_variants", "hidden", 0);
			frm.set_df_property("custom_combo_items_html", "hidden", 1);
		}

		if (frm.doc.has_variants) {
			frm.set_df_property("custom_is_combo", "hidden", 1);
			frm.set_df_property("custom_variant_details_html", "hidden", 0);
			frm.set_value("custom_is_combo", 0);
		} else {
			frm.set_df_property("custom_is_combo", "hidden", 0);
			frm.set_df_property("custom_variant_details_html", "hidden", 1);
		}

		inno_erp.item.combo_items.render_combo_items(frm);
		inno_erp.item.variant_details.render_variant_details(frm);

		if (frm.doc.variant_based_on === "Item Attribute") {
			frm.remove_custom_button(__("Single Variant"), __("Create"));
			frm.add_custom_button(
				__("Single Variant"),
				function () {
					inno_erp.item.item_dialog.show_single_variant_dialog(frm);
				},
				__("Create")
			);

			frm.remove_custom_button(__("Multiple Variants"), __("Create"));
			frm.add_custom_button(
				__("Multiple Variants"),
				function () {
					inno_erp.item.item_dialog.show_multiple_variants_dialog(frm);
				},
				__("Create")
			);
		}

		frm.add_custom_button(
			__("Create Omni"),
			() => {
				frappe.model.open_mapped_doc({
					method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.make_omni_item",
					frm: frm,
				});
			},
			__("Create")
		);
	},
	stock_uom: (frm) => {
		frm.set_value("weight_uom", frm.doc.stock_uom);
	},
	item_group: (frm) => {
		set_item_code(frm);
	},
	brand: (frm) => {
		set_item_code(frm);
	},
	has_variants: (frm) => {
		if (frm.doc.has_variants) {
			frm.set_df_property("standard_rate", "hidden", 1);
			return;
		}
		frm.set_df_property("standard_rate", "hidden", 0);
		frm.set_value("standard_rate", null);
	},
	before_save: (frm) => {
		if (frm.doc.custom_is_combo) {
			if (frm.is_new()) {
				frm.__is_new_record = true;
			}
			if (frm.combo_viewer) {
				frm.combo_viewer.sync_table_to_form();
			}
		}
		inno_erp.item.variant_details.prepare_data_for_save(frm);
	},
	after_save: (frm) => {
		if (frm.__is_new_record && frm.doc.custom_is_combo) {
			frm.reload_doc();
		}
	},
	custom_is_combo: (frm) => {
		inno_erp.item.combo_items.toggle_combo_items(frm);
	},
	is_stock_item: (frm) => {
		if (frm.doc.is_stock_item === 1) {
			frm.set_value("custom_is_combo", 0);
		}
	},
	valuation_rate: (frm) => {
		inno_erp.item.variant_details.auto_fill_valuation_rates(frm);
	},
});

function set_item_code(frm) {
	frappe.call({
		method: "inno_erp.inno_stock.overrides.item.item.get_item_code",
		args: {
			item_group: frm.doc.item_group,
			brand: frm.doc.brand,
		},
		async: false,
		callback: (r) => {
			frm.set_value("item_code", r.message);
			frm.set_value("item_name", r.message);
		},
	});
}
