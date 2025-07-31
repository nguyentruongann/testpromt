frappe.ui.form.on("Google Drive", {
	onload: function (frm) {
		if (frappe.user.has_role("System Manager")) {
			frm.page.add_action_item(__("Sync Google Drive"), function () {
				sync_google_drive_folders(frm);
			});
		}
	},
});

function sync_google_drive_folders() {
	frappe.confirm(
		__(
			"Are you sure you want to sync all folders from Google Drive?<br><br><strong>Note:</strong> This process may take a few minutes and will download the entire folder structure from Google Drive to ERPNext."
		),
		function () {
			frappe.show_alert({
				message: __("Starting to sync Google Drive..."),
				indicator: "blue",
			});

			let progress_dialog = new frappe.ui.Dialog({
				title: __("Sync Google Drive"),
				indicator: "blue",
				fields: [
					{
						fieldtype: "HTML",
						fieldname: "progress_html",
						options: __(`
                            <div class="progress-container">
                                <div class="progress-message py-3">
                                    <i class="fa fa-spin fa-spinner"></i>
                                    <span style="margin-left: 10px;">Connecting to Google Drive...</span>
                                </div>

                            </div>
                        `),
					},
				],
				primary_action_label: __("Runs in the background"),
				primary_action: function () {
					progress_dialog.hide();
					frappe.show_alert({
						message: __(
							"Sync is running in the background. You will receive a notification when it is complete."
						),
						indicator: "blue",
					});
				},
			});

			progress_dialog.show();

			frappe
				.call({
					method: "inno_vclshop.inno_vclshop.overrides.file.file.sync_google_drive_folders",
				})
				.then(() => {
					progress_dialog.hide();
				});
		}
	);
}
