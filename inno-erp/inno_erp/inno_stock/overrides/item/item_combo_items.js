frappe.provide("inno_erp.item.combo_items");
inno_erp.item.combo_items = {
	render_combo_items: (frm) => {
		frm.combo_area = $(frm.fields_dict.custom_combo_items_html.wrapper);
		frm.combo_area.empty();

		if (frm.doc.custom_is_combo) {
			frm.toggle_display("custom_combo_items_html", frm.doc.custom_is_combo);
			if (!frm.is_new()) {
				frappe.db
					.get_doc("Product Bundle", frm.doc.name)
					.then((doc) => {
						frm.doc.combo_items = doc.items || [];
						frm.refresh_field("combo_items");
						frm.combo_viewer = new inno_erp.item.ComboItemTable(frm.combo_area, frm);
					})
					.catch((error) => {
						frappe.msgprint({
							title: __("Error"),
							indicator: "red",
							message: __("Failed to fetch Product Bundle: ") + error,
						});
					});
			} else {
				frm.combo_viewer = new inno_erp.item.ComboItemTable(frm.combo_area, frm);
			}
		}
	},

	toggle_combo_items: (frm) => {
		frm.toggle_display("custom_combo_items_html", frm.doc.custom_is_combo);
		frm.set_value("is_stock_item", 0);
		if (frm.doc.custom_is_combo) {
			frm.refresh();
			frm.set_df_property("has_variants", "hidden", 1);
			frm.set_value("has_variants", 0);
		} else {
			frm.set_df_property("has_variants", "hidden", 0);
		}
	},
};

inno_erp.item.ComboItemTable = class {
	constructor(wrapper, frm) {
		this.wrapper = wrapper;
		this.frm = frm;

		this.combo_viewer = frappe.ui.form.make_control({
			parent: wrapper,
			df: {
				fieldname: "combo_items",
				fieldtype: "Table",
				label: __("<strong>Combo Items</strong>"),
				options: "Item",
				fields: [
					{
						fieldtype: "Link",
						fieldname: "item_code",
						label: "Item Code",
						options: "Item",
						in_list_view: 1,
						required: 1,
						get_query: function () {
							return {
								filters: {
									custom_is_combo: 0,
								},
							};
						},
						onchange: function () {
							frm.dirty();
							frappe.call({
								method: "frappe.client.get_value",
								args: {
									doctype: "Item",
									fieldname: ["stock_uom", "description"],
									filters: {
										item_code: this.value,
									},
								},
								callback: (r) => {
									if (r.message) {
										this.grid_row.on_grid_fields_dict.uom.set_value(
											r.message.stock_uom
										);
										this.grid_row.on_grid_fields_dict.description.set_value(
											r.message.description
										);
									}
								},
							});
						},
					},
					{
						fieldtype: "Int",
						fieldname: "qty",
						label: "Qty",
						in_list_view: 1,
						required: 1,
						default: 1,
						onchange: function () {
							frm.dirty();
						},
					},
					{
						fieldtype: "Data",
						fieldname: "description",
						label: "Description",
						in_list_view: 1,
						required: 1,
						onchange: function () {
							frm.dirty();
						},
					},
					{
						fieldtype: "Link",
						fieldname: "uom",
						label: "UOM",
						options: "UOM",
						in_list_view: 1,
						onchange: function () {
							frm.dirty();
						},
					},
				],
			},
			render_input: true,
		});
		this.reset();
		this.combo_viewer.refresh();
		$(this.combo_viewer.grid.wrapper).on("click", ".grid-remove-rows", () => {
			this.frm.dirty();
		});
	}

	reset() {
		const original_items = this.frm.doc.combo_items || [];
		this.combo_viewer.df.data = original_items;
	}

	destroy() {
		this.wrapper.empty();
		this.combo_viewer = null;
	}

	sync_table_to_form() {
		const rows = this.combo_viewer.get_value() || [];
		const valid_rows = rows.filter((r) => r.item_code);
		this.frm.doc.combo_items = valid_rows;
		this.frm.refresh_field("combo_items");
	}
};
