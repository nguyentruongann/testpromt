frappe.listview_settings["Item Price"] = {
	onload: (listview) => {
		listview.page.add_inner_button(__("Batch Update"), () => {
			const d = new frappe.ui.Dialog({
				title: __("Batch Update"),
				fields: [
					{
						fieldname: "price_list",
						label: __("Price List"),
						fieldtype: "Link",
						options: "Price List",
						reqd: 1,
					},
					{
						fieldname: "item_groups",
						label: __("Item Groups"),
						fieldtype: "Table MultiSelect",
						options: "Has Item Group",
						depends_on: "eval: doc.reference_method == 2",
						mandatory_depends_on: "eval: doc.reference_method == 2",
						onchange: (e) => {
							reset_dialog(d);
						},
					},

					{
						fieldname: "reference_price_list",
						label: __("Reference Price List"),
						fieldtype: "Link",
						options: "Price List",
						depends_on: "eval: doc.reference_method == 1",
						mandatory_depends_on: "eval: doc.reference_method == 1",
						get_query() {
							const price_list = d.fields_dict.price_list.value;
							return {
								filters: {
									name: ["!=", price_list],
								},
							};
						},
					},
					{
						fieldname: "all_update",
						// label: __('Tạo mới toàn bộ theo bảng giá tham chiếu'),
						label: __("Create new all according to the reference price list"),
						fieldtype: "Check",
						depends_on: "eval: doc.reference_method == 1",
					},
					{
						fieldname: "sdsfds",
						fieldtype: "Column Break",
					},
					{
						label: __("Method"),
						fieldname: "reference_method",
						fieldtype: "Select",
						options: [
							"",
							{ label: "Tham chiếu bảng giá cũ", value: 1 },
							{ label: "Theo nhóm hàng hóa", value: 2 },
						],
					},
					{
						label: __("Valid From"),
						fieldname: "valid_from",
						fieldtype: "Date",
						default: frappe.datetime.nowdate(),
						reqd: 1,
					},
					{
						label: __("Advanced Setting"),
						fieldname: "sdsssss",
						fieldtype: "Section Break",
						depends_on: "eval: doc.reference_method == 1",
					},
					{
						label: __("Plus"),
						fieldname: "plus",
						fieldtype: "Check",
						default: 1,
						onchange: (e) => {
							if (e) {
								d.set_value("minus", 0);
							}
						},
					},

					{
						label: __("Minus"),
						fieldname: "minus",
						fieldtype: "Check",
						onchange: (e) => {
							if (e) {
								d.set_value("plus", 0);
							}
						},
					},
					{
						fieldname: "sdsdddfds",
						fieldtype: "Column Break",
					},
					{
						label: __("Percent"),
						fieldname: "percent",
						fieldtype: "Check",
						default: 1,
						onchange: (e) => {
							if (e) {
								d.set_value("plus", 0);
							}
						},
					},
					{
						label: __("Price"),
						fieldname: "rate",
						fieldtype: "Check",

						onchange: (e) => {
							if (e) {
								d.set_value("minus", 0);
							}
						},
					},
					{
						fieldname: "sdsdddfds",
						fieldtype: "Column Break",
					},
					{
						label: __("Value"),
						fieldname: "value",
						fieldtype: "Float",
						mandatory_depends_on: "eval: doc.reference_method == 1",
					},
					{
						fieldname: "sdsddaâdfds",
						fieldtype: "Section Break",
					},
					{
						fieldname: "items",
						fieldtype: "Table",
						depends_on: "eval: doc.reference_method != 1",
						mandatory_depends_on: "eval: doc.reference_method != 1",
						fields: [
							{
								label: __("Item Code"),
								fieldname: "item_code",
								fieldtype: "Link",
								options: "Item",
								in_list_view: 1,
								reqd: 1,
								columns: 2,
								change: () => {
									const item_code = this.get_value();
									const row = this;
									if (item_code) {
										frappe.db
											.get_value("Item", item_code, "item_name")
											.then((r) => {
												if (r.message) {
													row.grid_row.on_grid_fields_dict.item_name.set_value(
														r.message.item_name,
													);
												}
											});
									}
								},
							},
							{
								label: __("Item Name"),
								fieldname: "item_name",
								fieldtype: "Data",
								in_list_view: 1,
								read_only: 1,
								columns: 2,
							},
							{
								label: __("Rate"),
								fieldname: "rate",
								fieldtype: "Float",
								in_list_view: 1,
								columns: 2,
							},
						],
					},
				],
				primary_action_label: "Submit",
				primary_action(values) {
					frappe.call({
						method:
							"inno_erp.inno_stock.overrides.item_price.item_price.create_multi_item_price",
						args: {
							reference_method: values.reference_method,
							reference_price_list: values.reference_price_list || "",
							items: values.items || [],
							operator: values.plus ? "+" : values.minus ? "-" : "",
							variance: values.percent ? "%" : values.rate ? "rate" : "",
							value: values.value || 0,
							price_list: values.price_list,
							valid_from: values.valid_from,
							all_update: values.all_update || "",
						},
						freeze: true,
						freeze_message: __("Creating ..."),
						callback: (r) => {
							d.hide();
						},
					});
				},
			});
			d.show();
			d.$wrapper.find(".modal-dialog").css("max-width", "80vw");
		});
	},
};

function reset_dialog(dialog) {
	const fields = dialog.fields_dict;
	fields.items.df.data = [];
	fields.items.grid.refresh();
	if (fields.item_groups.value) {
		frappe.call({
			method:
				"inno_erp.inno_stock.overrides.item_price.item_price.get_items_by_item_groups",
			args: {
				item_groups: fields.item_groups.value,
			},
			callback: (r) => {
				$.each(r.message || [], (i, d) => {
					fields.items.df.data.push({
						item_code: d.name,
						item_name: d.item_name,
					});
				});
				fields.items.grid.refresh();
			},
		});
	}
}
