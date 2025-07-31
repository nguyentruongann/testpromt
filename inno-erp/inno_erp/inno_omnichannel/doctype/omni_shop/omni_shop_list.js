frappe.listview_settings["Omni Shop"] = {
	onload: function (listview) {
		listview.page.add_inner_button(__("Link Account"), function () {
			show_link_account_dialog();
		});
	},
};

const show_link_account_dialog = () => {
	let dialog = new frappe.ui.Dialog({
		title: __("Link Platform Account"),
		size: "medium",
		fields: [
			{
				fieldname: "platform",
				label: __("Platform"),
				fieldtype: "Select",
				options: [
					{ label: __("Lazada"), value: "LAZADA" },
					{ label: __("TikTok Shop"), value: "TIKTOK_SHOP" },
					{ label: __("Shopee"), value: "SHOPEE" },
				],
				reqd: 1,
				description: __("Select the platform you want to link your account to"),
			},
		],
		primary_action: function (values) {
			frappe.call({
				method: "inno_erp.controller.omni.oauth_authorize",
				args: {
					platform: values.platform,
				},
				callback: function (r) {
					if (r.message) {
						// Open Lazada authorization URL in new window
						window.open(r.message, "_blank", "width=1024,height=1024");

						frappe.msgprint({
							message: __(
								"Please complete the authorization in the new window. You will be redirected back once completed."
							),
							title: __("Authorization Required"),
							indicator: "blue",
						});
					}
				},
				error: function (r) {
					frappe.msgprint({
						message: __("Failed to initiate Lazada authorization"),
						title: __("Error"),
						indicator: "red",
					});
				},
			});
		},
		primary_action_label: __("Link Account"),
		secondary_action_label: __("Cancel"),
		secondary_action: function () {
			dialog.hide();
		},
	});

	dialog.show();
};
