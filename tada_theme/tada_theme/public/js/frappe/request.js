frappe.provide("frappe.request");

frappe.request.report_error = (xhr, request_opts) => {
	const data = JSON.parse(xhr.responseText);
	let exc;
	if (data.exc) {
		try {
			exc = (JSON.parse(data.exc) || []).join("\n");
		} catch (e) {
			exc = data.exc;
		}
		// biome-ignore lint/performance/noDelete: <explanation>
		delete data.exc;
	} else {
		exc = "";
	}

	const copy_markdown_to_clipboard = () => {
		const code_block = (snippet) => `\`\`\`\n${snippet}\n\`\`\``;

		const request_data = Object.assign({}, request_opts);
		request_data.request_id = xhr.getResponseHeader("X-Frappe-Request-Id");
		const traceback_info = [
			"### App Versions",
			code_block(JSON.stringify(frappe.boot.versions, null, "\t")),
			"### Route",
			code_block(frappe.get_route_str()),
			"### Traceback",
			code_block(exc),
			"### Request Data",
			code_block(JSON.stringify(request_data, null, "\t")),
			"### Response Data",
			code_block(JSON.stringify(data, null, "\t")),
		].join("\n");
		frappe.utils.copy_to_clipboard(traceback_info);
	};

	const show_communication = () => {
		const error_report_message = [
			"<h5>Please type some additional information that could help us reproduce this issue:</h5>",
			'<div style="min-height: 100px; border: 1px solid #bbb; \
				border-radius: 5px; padding: 15px; margin-bottom: 15px;"></div>',
			"<hr>",
			"<h5>App Versions</h5>",
			`<pre>${JSON.stringify(frappe.boot.versions, null, "\t")}</pre>`,
			"<h5>Route</h5>",
			`<pre>${frappe.get_route_str()}</pre>`,
			"<hr>",
			"<h5>Error Report</h5>",
			`<pre>${exc}</pre>`,
			"<hr>",
			"<h5>Request Data</h5>",
			`<pre>${JSON.stringify(request_opts, null, "\t")}</pre>`,
			"<hr>",
			"<h5>Response JSON</h5>",
			`<pre>${JSON.stringify(data, null, "\t")}</pre>`,
		].join("\n");

		const communication_composer = new frappe.views.CommunicationComposer({
			subject: `Error Report [${frappe.datetime.nowdate()}]`,
			recipients: error_report_email,
			message: error_report_message,
			doc: {
				doctype: "User",
				name: frappe.session.user,
			},
		});
		communication_composer.dialog.$wrapper.css(
			"z-index",
			cint(frappe.msg_dialog.$wrapper.css("z-index")) + 1,
		);
	};

	if (exc) {
		const error_report_email = frappe.boot.error_report_email;

		request_opts = frappe.request.cleanup_request_opts(request_opts);

		// window.msg_dialog = frappe.msgprint({message:error_message, indicator:'red', big: true});

		if (!frappe.error_dialog) {
			frappe.error_dialog = new frappe.ui.Dialog({
				title: __("Server Error"),
			});

			// By Tada: Commenting out the error report email functionality
			// if (error_report_email) {
			//     frappe.error_dialog.set_primary_action(__("Report"), () => {
			//         show_communication();
			//         frappe.error_dialog.hide();
			//     });
			// } else {
			//     frappe.error_dialog.set_primary_action(__("Copy error to clipboard"), () => {
			//         copy_markdown_to_clipboard();
			//         frappe.error_dialog.hide();
			//     });
			// }
			frappe.error_dialog.wrapper.classList.add("msgprint-dialog");
		}

		const parts = strip(exc).split("\n");

		let dialog_html = parts[parts.length - 1];

		if (data._exc_source) {
			dialog_html += "<br>";
			// By Tada: Commenting out the error report email functionality
			// dialog_html += `Possible source of error: ${data._exc_source.bold()} `;
		}

		frappe.error_dialog.$body.html(dialog_html);
		frappe.error_dialog.show();
	}
};
