frappe.provide("frappe.ui.form");

frappe.ui.form.ControlAttachImage = class TadaControlAttachImage extends frappe.ui.form.ControlAttachImage {
	clear_attachment() {
		let me = this;
		frappe.confirm(__("Are you sure you want to delete the attachment?"), function () {
			if (me.frm) {
				me.parse_validate_and_set_in_model(null);
				me.refresh();
				me.frm.attachments.remove_attachment_by_filename(me.value, async () => {
					await me.parse_validate_and_set_in_model(null);
					me.refresh();
				});
			} else {
				me.dataurl = null;
				me.fileobj = null;
				me.set_input(null);
				me.parse_validate_and_set_in_model(null);
				me.refresh();
			}
		});
	}

	async on_upload_complete(attachment) {
		if (this.frm) {
			await this.parse_validate_and_set_in_model(attachment.file_url);
			this.frm.attachments.update_attachment(attachment);
		}
		this.set_value(attachment.file_url);
	}
};
