frappe.listview_settings["Omni Item"] = {
	add_fields: [
		"stock_uom",
		"has_variants",
		"disabled",
		"variant_of",
		"item_code",
		"waiting_orders",
	],
	button: {
		show: function (doc) {
			return true;
		},
		get_label: function (doc) {
			return __("Link");
		},
		get_description: function (doc) {
			return doc.linked_item
				? __("Current: {0}", [doc.linked_item])
				: __("Link to ERP Item");
		},
		action: function (doc) {
			show_link_dialog(doc);
		},
	},
	get_indicator: (doc) => {
		if (doc.disabled) {
			return [__("Disabled"), "grey", "disabled,=,Yes"];
		}
		if (doc.waiting_orders) {
			return [__("Waiting Orders"), "red", "waiting_orders,>,0"];
		}
		if (doc.end_of_life && doc.end_of_life < frappe.datetime.get_today()) {
			return [__("Expired"), "grey", "end_of_life,<,Today"];
		}
		if (doc.has_variants) {
			return [__("Template"), "orange", "has_variants,=,Yes"];
		}
		if (doc.variant_of) {
			return [__("Variant"), "green", `variant_of,=,${doc.variant_of}`];
		}
	},
};

const show_link_dialog = (doc) => {
	let dialog = new frappe.ui.Dialog({
		title: __("Link Item"),
		size: "large",
		fields: [
			{
				fieldname: "filter_by",
				label: __("Filter By"),
				fieldtype: "Section Break",
			},
			{
				fieldname: "column_break",
				fieldtype: "Column Break",
			},
			{
				fieldname: "item_group",
				label: __("Item Group"),
				fieldtype: "Link",
				options: "Item Group",
				default: doc.item_group || "",
			},
			{
				fieldname: "column_break2",
				fieldtype: "Column Break",
			},
			{
				fieldname: "brand",
				label: __("Brand"),
				fieldtype: "Link",
				options: "Brand",
				default: doc.brand || "",
			},
			{
				fieldname: "filter_by2",
				fieldtype: "Section Break",
			},
			{
				fieldname: "linked_item",
				label: __("Item"),
				fieldtype: "Link",
				options: "Item",
				description: __("Select the ERP item to link to this Omni Item"),
				default: doc.linked_item || "",
				get_query: () => {
					return {
						query: "inno_erp.inno_stock.overrides.item.item.get_items_by_item_group_and_brand",
						filters: {
							item_group: dialog.get_value("item_group"),
							brand: dialog.get_value("brand"),
							variant_of: doc.variant_of,
						},
					};
				},
			},
		],
		primary_action: function (values) {
			frappe.call({
				method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.update_linked_item",
				args: {
					doc_name: doc.name,
					linked_item: values.linked_item,
				},
				callback: function (r) {
					if (r.message) {
						frappe.msgprint({
							message: r.message,
							title: __("Success"),
							indicator: "green",
						});
					}
					dialog.hide();
					cur_list.refresh();
				},
			});
		},
		primary_action_label: __("Link"),
		secondary_action_label: __("Cancel"),
		secondary_action: function () {
			dialog.hide();
		},
	});

	dialog.show();
};
