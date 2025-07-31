// Copyright (c) 2025, Tada Labs and contributors
// For license information, please see license.txt

frappe.ui.form.on("Omni Item", {
	refresh(frm) {
		if (!frm.is_new()) {
			frm.page.add_inner_button(__("Crawl URL"), () => {
				crawl_item_dialog(frm).show();
			});
		}
		frm.set_query('custom_upload_media', function() {
            return {
                filters: {
                    'is_folder': 1
                }
            };
        });
		frm.set_query('custom_upload_media_360', function() {
            return {
                filters: {
                    'is_folder': 1
                }
            };
        });
	},
});

function crawl_item_dialog(frm) {
	let dialog = new frappe.ui.Dialog({
		title: __("Crawl URL"),
		size: "small",
		static: true,
		fields: [
			{
				fieldname: "item_url",
				fieldtype: "Data",
				label: __("URL"),
				reqd: 1,
			},
		],
		primary_action_label: __("Execute"),
		primary_action: () => {
			let dialog_values = dialog.get_values();
			url = dialog_values.item_url;
			if (!url) {
				frappe.msgprint(__("Please enter a valid item URL"));
				return;
			}
			frappe.call({
				method: "inno_vclshop.inno_vclshop.overrides.omni_item.omni_item.fetch_item_from_url",
				freeze: true,
				freeze_message: __("Crawling ..."),
				args: {
					item_url: url,
					item_code: frm.doc.item_code,
				},
				callback: (r) => {
					if (r.message) {
						frm.refresh();
						dialog.hide();
					} else {
						frappe.msgprint(__("Failed to fetch item from URL"));
					}
				},
			});
		},
		secondary_action_label: __("Cancel"),
		secondary_action: () => {
			dialog.hide();
		},
	});

	return dialog;
}



