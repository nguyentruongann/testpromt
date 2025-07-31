frappe.provide("inno.sales_invoice");

inno.sales_invoice.open_payment_dialog = async (frm) => {
	try {
		const res = await frappe.db.get_list("Mode of Payment", {
			fields: ["name"],
			filters: { enabled: 1 },
		});
		const mode_of_payments = res.map((item) => item.name);
		const payment_methods = ["PHYSICAL CARD", "QR CODE"];

		const payment_dialog = new frappe.ui.Dialog({
			title: __("Payment for {0}", [frm.doc.name]),
			fields: [
				{
					label: __("Customer"),
					fieldname: "customer",
					fieldtype: "Data",
					default: frm.doc.customer_name || "",
					read_only: 1,
				},
				{
					label: __("Amount"),
					fieldname: "amount",
					fieldtype: "Currency",
					default: frm.doc.rounded_total || 0,
					read_only: 1,
				},
				{
					label: "Mode of Payment",
					fieldname: "mode_of_payment",
					fieldtype: "Select",
					reqd: 1,
					options: mode_of_payments,
					default: mode_of_payments[0] || "",
					onchange: function () {
						onchange_mode_or_method();
					},
				},
				{
					label: __("Payment Method"),
					fieldname: "payment_method",
					fieldtype: "Select",
					default: payment_methods[0] || "",
					options: payment_methods,
					onchange: function () {
						onchange_mode_or_method();
					},
				},
				{
					label: __("QR Code"),
					fieldname: "qr_code",
					fieldtype: "HTML",
				},
				{
					label: __("Create Payoo Order"),
					fieldname: "create_payoo_order",
					fieldtype: "Button",
				},
			],
			primary_action_label: __("Submit"),
			primary_action(values) {
				const mode = payment_dialog.get_value("mode_of_payment");
				const method = payment_dialog.get_value("payment_method");
				payoo_order = frappe.model.get_value("Payoo Order", {
					parent: frm.doc.name,
					payment_method: values.payment_method,
					status_code: 0,
				});
				frappe.call({
					method: "inno_erp.inno_account.overrides.sales_invoice.sales_invoice.submit_sales_invoice",
					args: {
						sales_invoice_name: frm.doc.name,
						mode_of_payment: mode,
						payment_method: method || "",
						amount: frm.doc.rounded_total,
					},
					callback: function (r) {
						if (r.message.success === 0) {
							frappe.throw(r.message.message);
						} else {
							frappe.msgprint(r.message.message);
							payment_dialog.hide();
						}
					},
				});
			},
		});

		payment_dialog.show();

		async function onchange_mode_or_method() {
			payment_dialog.fields_dict.qr_code.$wrapper.html("");
			const mode = payment_dialog.get_value("mode_of_payment");
			const method = payment_dialog.get_value("payment_method");
			const show_payment_method = [__("Payoo")].includes(mode);
			const show_qr =
				([__("Payoo")].includes(mode) && ["QR CODE"].includes(method)) ||
				[__("Wire Transfer")].includes(mode);

			payment_dialog.set_df_property("payment_method", "hidden", !show_payment_method);
			payment_dialog.set_df_property("qr_code", "hidden", !show_qr);
			payment_dialog.set_df_property("create_payoo_order", "hidden", true);

			if (mode === __("Payoo")) {
				let payment_method = method === "QR CODE" ? 2 : 0;
				payment_dialog.set_df_property("create_payoo_order", "hidden", false);
				payment_dialog.fields_dict.create_payoo_order.$input
					.off("click")
					.on("click", async () => {
						const r = await frappe.call({
							method: "inno_erp.controller.payoo.create_payment_request",
							args: {
								sales_invoice_name: frm.doc.name,
								payment_method: payment_method,
							},
						});
						const order = r.message;
						frappe.msgprint(__("Payoo Order created successfully."));
					});
			}

			if (mode === __("Wire Transfer")) {
				const r = await frappe.call({
					method: "inno_erp.controller.payoo.get_bank_qr_code_url",
					args: {
						sales_invoice_name: frm.doc.name,
					},
				});

				payment_dialog.fields_dict.qr_code.$wrapper.html(`
                    <div style="text-align:center; margin-top:10px;">
                        <img src="${r.message}" style="max-width:400px; border:1px solid #ccc;">
                    </div>
                `);
			}
		}

		await onchange_mode_or_method();
	} catch (error) {
		console.error("Error opening payment dialog:", error);
		frappe.msgprint("Cannot open payment dialog. Please try again later.");
	}
};
