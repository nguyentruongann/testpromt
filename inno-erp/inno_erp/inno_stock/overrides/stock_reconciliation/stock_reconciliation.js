frappe.ui.form.on("Stock Reconciliation", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_session(frm);
		}

		frm.get_field("items").grid.add_custom_button(__("View History"), function () {
			show_dialog(frm);
		});
	},
	refresh: (frm) => {
		frm.toggle_display("company", 0);
		highlight_child_table(frm.get_field("items").grid.grid_rows);
		frm.get_field("items").grid.toggle_enable("warehouse", false);
	},
	company: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_session(frm);
		}
	},
	custom_get_items: (frm) => {
		const d = new frappe.ui.Dialog({
			title: __("Get Items"),
			size: "large",
			fields: [
				{
					fieldname: "item_groups",
					label: __("Item Group"),
					fieldtype: "Table MultiSelect",
					options: "Has Item Group",
				},
			],
			primary_action_label: "Submit",
			primary_action(values) {
				if (values.item_groups) {
					frappe.call({
						method: "inno_erp.inno_stock.overrides.item.item.get_items_by_item_groups",
						args: {
							item_groups: values.item_groups,
						},
						freeze: true,
						freeze_message: __("Loading ..."),
						callback: (r) => {
							$.each(r.message || [], (i, d) => {
								const row = frm.add_child("items", {
									item_code: d.name,
									item_name: d.item_name,
									item_group: d.item_group,
									warehouse: frm.doc.set_warehouse,
								});
								frm.trigger("warehouse", "Stock Reconciliation Item", row.name);
								frm.trigger("qty", "Stock Reconciliation Item", row.name);
							});
							frm.refresh_field("items");
							d.hide();
						},
					});
				}
			},
		});
		d.show();
	},
});

frappe.ui.form.on("Stock Reconciliation Item", {
	qty: (frm, cdt, cdn) => {
		const d = frappe.model.get_doc(cdt, cdn);
		frappe.model.set_value(
			cdt,
			cdn,
			"quantity_difference",
			Math.abs((d.qty || 0) - d.current_qty)
		);
	},
	current_qty: (frm, cdt, cdn) => {
		const d = frappe.model.get_doc(cdt, cdn);
		frappe.model.set_value(
			cdt,
			cdn,
			"quantity_difference",
			Math.abs((d.qty || 0) - (d.current_qty || 0))
		);
	},
	amount_difference: (frm, cdt, cdn) => {
		frm.refresh_field("items");
		const grid_row = frm.get_field("items").grid.grid_rows_by_docname[cdn];
		highlight_child_table([grid_row]);
	},
	quantity_difference: (frm, cdt, cdn) => {
		frm.refresh_field("items");
		const grid_row = frm.get_field("items").grid.grid_rows_by_docname[cdn];
		highlight_child_table([grid_row]);
	},
});

const highlight_child_table = (rows = []) => {
	$.each(rows || [], (i, row) => {
		const $row = $(row.wrapper);

		if (row.doc.amount_difference || Number.parseFloat(row.doc.quantity_difference)) {
			$row.removeClass("highlight-stock-green");
			$row.addClass("highlight-stock-red");
		} else {
			$row.removeClass("highlight-stock-red");
			$row.addClass("highlight-stock-green");
		}
	});
};

const show_dialog = (frm) => {
	const dialog = new frappe.ui.Dialog({
		title: __("Item History"),
		size: "extra-large",
		fields: [
			{
				fieldtype: "Section Break",
			},
			{
				fieldname: "orders",
				label: __("Orders"),
				fieldtype: "Table",
				data: [],
				cannot_add_rows: true,
				cannot_delete_rows: true,
				get_data: (doc, cdt, cdn) => {
					return doc.orders;
				},
				fields: [
					{
						fieldname: "reference_type",
						label: __("Type"),
						fieldtype: "Link",
						options: "DocType",
						read_only: 1,
					},
					{
						fieldname: "order",
						label: __("Order"),
						fieldtype: "Dynamic Link",
						options: "reference_type",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "item_code",
						label: __("Item Code"),
						fieldtype: "Link",
						options: "Item",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "creation",
						label: __("Creation"),
						fieldtype: "Date",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "delivery_date",
						label: __("Delivery Date"),
						fieldtype: "Date",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "qty",
						label: __("Qty"),
						fieldtype: "Data",
						in_list_view: 1,
						read_only: 1,
					},
				],
			},
			{
				fieldtype: "Section Break",
			},
			{
				fieldname: "purchases",
				label: __("Purchases"),
				fieldtype: "Table",
				data: [],
				cannot_add_rows: true,
				cannot_delete_rows: true,
				get_data: (doc, cdt, cdn) => {
					return doc.purchases;
				},
				fields: [
					{
						fieldname: "purchase",
						label: __("Purchase"),
						fieldtype: "Link",
						options: "Purchase Invoice",
						in_list_view: 1,
					},
					{
						fieldname: "item_code",
						label: __("Item Code"),
						fieldtype: "Link",
						options: "Item",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "due_date",
						label: __("Due Date"),
						fieldtype: "Date",
						in_list_view: 1,
						read_only: 1,
					},
					{
						fieldname: "qty",
						label: __("Qty"),
						fieldtype: "Data",
						in_list_view: 1,
						read_only: 1,
					},
				],
			},
		],
	});

	get_history_of_items(frm, dialog);
	dialog.show();

	return dialog;
};

const get_history_of_items = (frm, dialog) => {
	const selected_items = frm.get_field("items").grid.get_selected();
	const item_codes = frm.doc.items
		.filter((item) => selected_items.includes(item.name) && item.item_code != null)
		.map((item) => item.item_code);

	if (item_codes.length === 0) {
		return;
	}

	frappe.call({
		method: "inno_erp.inno_stock.overrides.stock_reconciliation.stock_reconciliation.get_history_of_items",
		args: {
			item_codes: item_codes,
			warehouse: frm.doc.set_warehouse,
		},
		callback: (r) => {
			if (r.message) {
				if (r.message.orders) {
					dialog.fields_dict.orders.grid.df.data = r.message.orders;
					dialog.fields_dict.orders.grid.refresh();
				}
				if (r.message.purchases) {
					dialog.fields_dict.purchases.grid.df.data = r.message.purchases;
					dialog.fields_dict.purchases.grid.refresh();
				}
			}
		},
	});
};
