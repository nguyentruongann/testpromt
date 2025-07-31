frappe.provide("inno_erp.item.variant_details");
inno_erp.item.variant_details = {
	render_variant_details: (frm) => {
		frm.variant_details_area = $(frm.fields_dict.custom_variant_details_html.wrapper);
		frm.variant_details_area.empty();

		// Get variant count
		frappe.call({
			method: "frappe.client.get_list",
			args: {
				doctype: "Item",
				filters: {
					variant_of: frm.doc.name,
				},
				fields: ["name"],
			},
			callback: function (countResponse) {
				try {
					frm.variant_count = countResponse.message ? countResponse.message.length : 0;

					if (frm.variant_count > 0) {
						// Hide has_variants
						frm.set_df_property("has_variants", "hidden", 1);
						frm.set_df_property("has_variants", "read_only", 1);
					}

					if (frm.doc.has_variants && !frm.is_new() && frm.variant_count > 0) {
						frm.toggle_display("custom_variant_details_html", true);
						frm.doc.__variant_details = [];
						frm.doc.__origin_variant_details = [];
						frm.doc.__deleted_variant_details = [];

						// Get detail variants
						frappe.call({
							method: "inno_erp.inno_stock.overrides.item.item.get_detail_variants",
							args: {
								template_item_code: frm.doc.item_code,
							},
							callback: function (detailResponse) {
								if (
									detailResponse.message &&
									detailResponse.message.status === "success"
								) {
									let rows = detailResponse.message.rows || [];
									if (rows.length === 0) {
										return;
									}
									frm.doc.__variant_details = rows;
									frm.doc.__origin_variant_details = rows;
									frm.variant_details_viewer =
										new inno_erp.item.VariantDetailsTable(
											frm.variant_details_area,
											frm
										);
									inno_erp.item.variant_details.update_template_valuation_rate_to_variant(frm);
									inno_erp.item.variant_details.update_selling_rates_by_refresh(frm);
								} else if (
									detailResponse.message &&
									detailResponse.message.status === "error"
								) {
									frappe.msgprint(
										__("Error loading variant data: {0}", [
											detailResponse.message?.message || "Unknown error",
										])
									);
								}
							},
							error: function (error) {
								frappe.msgprint(__("Error loading variant data"));
							},
						});
					} else {
						frm.toggle_display("custom_variant_details_html", false);
					}
				} catch (error) {
					frappe.msgprint(__("Error loading variant data"));
				}
			},
			error: function (error) {
				frappe.msgprint(__("Error loading variant data"));
			},
		});
	},

	update_valuation_rates(row, frm) {
		if (!row || !row.doc) {
			return;
		}

		if (!row.doc.is_base_uom) return;

		let new_base_valuation_rate = row.doc.valuation_rate || 0;
		let current_variant_code = row.doc.variant_item_code;

		let variant_details = frm.variant_details_viewer.viewer.get_value() || [];

		for (const detail of variant_details) {
			if (detail.variant_item_code === current_variant_code && !detail.is_base_uom) {
				detail.valuation_rate = new_base_valuation_rate * (detail.conversion_factor || 1);
				detail.base_valuation_rate = new_base_valuation_rate;
			}
		}

		frm.variant_details_viewer.viewer.df.data = variant_details;
		frm.variant_details_viewer.viewer.refresh();
	},

	update_selling_rates(row, frm) {
		if (!row || !row.doc) {
			return;
		}

		if (!row.doc.is_base_uom) return;

		let new_base_selling_rate = row.doc.selling_rate || 0;
		let current_variant_code = row.doc.variant_item_code;

		let variant_details = frm.variant_details_viewer.viewer.get_value() || [];

		for (const detail of variant_details) {
			if (detail.variant_item_code === current_variant_code && !detail.is_base_uom) {
				detail.selling_rate = new_base_selling_rate * (detail.conversion_factor || 1);
			}
		}

		frm.variant_details_viewer.viewer.df.data = variant_details;
		frm.variant_details_viewer.viewer.refresh();
	},

	update_template_valuation_rate_to_variant(frm) {
		if (frm.doc.has_variants && frm.variant_details_viewer) {
			let variant_details = frm.variant_details_viewer.get_current_data();
			for (const detail of variant_details) {
				// Chỉ cập nhật nếu valuation_rate hiện tại là 0
				if (detail.valuation_rate == 0) {
					if (detail.is_base_uom) {
						detail.valuation_rate = frm.doc.valuation_rate;
						detail.base_valuation_rate = frm.doc.valuation_rate;
					} else {
						detail.valuation_rate = frm.doc.valuation_rate * (detail.conversion_factor || 1);
					}
				}
			}
			frm.variant_details_viewer.viewer.df.data = variant_details;
			frm.variant_details_viewer.viewer.refresh();
		}
	},

	update_selling_rates_by_refresh(frm) {
		if (frm.doc.has_variants && frm.variant_details_viewer) {
			let variant_details = frm.variant_details_viewer.get_current_data();

			// Lưu lại base selling_rate theo từng variant_item_code
			let base_selling_rate_map = {};
			let base_uom_map = {};

			// Duyệt lần 1: tìm base UOM cho từng variant_item_code
			for (const detail of variant_details) {
				if (detail.is_base_uom) {
					base_selling_rate_map[detail.variant_item_code] = detail.selling_rate;
					base_uom_map[detail.variant_item_code] = detail.uom;
				}
			}

			// Duyệt lần 2: cập nhật các dòng không phải base UOM
			for (const detail of variant_details) {
				if (
					!detail.is_base_uom &&
					base_selling_rate_map[detail.variant_item_code] !== undefined &&
					(!detail.selling_rate || detail.selling_rate == 0)
				) {
					detail.selling_rate = base_selling_rate_map[detail.variant_item_code] * (detail.conversion_factor || 1);
				}
			}

			frm.variant_details_viewer.viewer.df.data = variant_details;
			frm.variant_details_viewer.viewer.refresh();
		}
	},

	auto_fill_valuation_rates(frm) {
		if (frm.doc.has_variants && frm.variant_details_viewer) {
			let variant_details = frm.variant_details_viewer.get_current_data();
			for (const detail of variant_details) {
				if (detail.is_base_uom) {
					detail.valuation_rate = frm.doc.valuation_rate;
					detail.base_valuation_rate = frm.doc.valuation_rate;
				} else {
					detail.valuation_rate = frm.doc.valuation_rate * (detail.conversion_factor || 1);
				}
			}
			frm.variant_details_viewer.viewer.df.data = variant_details;
			frm.variant_details_viewer.viewer.refresh();
		}
	},

	prepare_data_for_save(frm) {
		if (frm.doc.has_variants && !frm.is_new() && frm.variant_count > 0) {
			frm.doc.__variant_details = frm.variant_details_viewer.get_current_data();

			let current_items = [];
			for (const v of frm.doc.__variant_details) {
				current_items.push(`${v.variant_item_code}_${v.uom}`);
			}
			frm.doc.__deleted_variant_details = [];
			for (const orig of frm.doc.__origin_variant_details) {
				if (!current_items.includes(`${orig.variant_item_code}_${orig.uom}`)) {
					frm.doc.__deleted_variant_details.push(orig);
				}
			}
		}
	},
};

inno_erp.item.VariantDetailsTable = class {
	constructor(wrapper, frm) {
		this.wrapper = wrapper;
		this.frm = frm;
		this.viewer = frappe.ui.form.make_control({
			parent: wrapper,
			df: {
				label: __("<b>Variant Details</b>"),
				fieldname: "variant_details",
				fieldtype: "Table",
				data: this.frm.doc.__variant_details || [],
				cannot_add_rows: true,
				in_place_edit: true,
				fields: [
					{
						fieldname: "variant_item_code",
						fieldtype: "Link",
						options: "Item",
						in_list_view: 1,
						label: __("Variant Item Code"),
						read_only: 1,
						columns: 3,
					},
					{
						fieldname: "uom",
						fieldtype: "Link",
						options: "UOM",
						in_list_view: 1,
						label: __("UOM"),
						read_only: 1,
						columns: 1,
					},
					{
						fieldname: "valuation_rate",
						fieldtype: "Currency",
						in_list_view: 1,
						label: __("Valuation Rate"),
						columns: 3,
						placeholder: __("Enter Valuation Rate"),
						onchange: function () {
							inno_erp.item.variant_details.update_valuation_rates(this.grid_row, frm);
							// make dirty
							frm.dirty();
						},
					},
					{
						fieldname: "selling_rate",
						fieldtype: "Currency",
						in_list_view: 1,
						label: __("Selling Rate"),
						columns: 3,
						placeholder: __("Enter Selling Rate"),
						onchange: function () {
							inno_erp.item.variant_details.update_selling_rates(this.grid_row, frm);
							// make dirty
							frm.dirty();
						},
					},
					{
						fieldname: "conversion_factor",
						fieldtype: "Float",
						label: __("Conversion Factor"),
						placeholder: __("Enter Conversion Factor"),
						read_only: 1,
						hidden: 1,
					},
					{
						fieldname: "is_base_uom",
						fieldtype: "Check",
						label: __("Is Base UOM"),
						read_only: 1,
						hidden: 1,
					},
				],
			},
			render_input: true,
		});
		this.viewer.refresh();
		$(this.viewer.grid.wrapper).on("click", ".grid-remove-rows", () => {
			this.frm.dirty();
		});
	}

	get_current_data() {
		return this.viewer.get_value() || [];
	}
};
