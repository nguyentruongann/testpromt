frappe.provide("frappe.ui.form");

frappe.ui.form.InnoContactAddressQuickEntryForm = class InnoContactAddressQuickEntryForm extends (
	frappe.ui.form.QuickEntryForm
) {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	}

	render_dialog() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		super.render_dialog();
	}

	insert() {
		/**
		 * Using alias fieldnames because the doctype definition define "email_id" and "mobile_no" as readonly fields.
		 * Therefor, resulting in the fields being "hidden".
		 */
		const map_field_names = {
			email_address: "email_id",
			mobile_number: "mobile_no",
		};

		// biome-ignore lint/complexity/noForEach: <explanation>
		Object.entries(map_field_names).forEach(([fieldname, new_fieldname]) => {
			this.dialog.doc[new_fieldname] = this.dialog.doc[fieldname];
			delete this.dialog.doc[fieldname];
		});

		return super.insert();
	}

	get_variant_fields() {
		const variant_fields = [
			{
				fieldtype: "Section Break",
				label: __("Primary Contact Details"),
				collapsible: 1,
			},
			{
				label: __("Email Id"),
				fieldname: "email_address",
				fieldtype: "Data",
				options: "Email",
			},
			{
				fieldtype: "Column Break",
			},
			{
				label: __("Mobile Number"),
				fieldname: "mobile_number",
				fieldtype: "Data",
			},
			{
				fieldtype: "Section Break",
				label: __("Primary Address Details"),
				collapsible: 1,
			},
			{
				label: __("Address Line 1"),
				fieldname: "address_line1",
				fieldtype: "Data",
			},
			{
				label: __("Address Location"),
				fieldname: "custom_address_location",
				fieldtype: "Link",
				options: "Address Location",
				change: () => {
					const template_type = this.dialog.get_value(
						"custom_address_location",
					);

					if (!template_type) {
						this.dialog.set_df_property("custom_address_ward", "hidden", 1);
						return;
					}

					this.dialog.set_df_property("custom_address_ward", "hidden", 0);
					this.dialog.set_df_property(
						"custom_address_ward",
						"get_query",
						() => {
							return {
								filters: [["Address Ward", "location", "=", template_type]],
							};
						},
					);
				},
			},
			{
				label: __("Ward"),
				fieldname: "custom_address_ward",
				fieldtype: "Link",
				options: "Address Ward",
				hidden: 1,
			},
			{
				label: __("Customer POS Id"),
				fieldname: "customer_pos_id",
				fieldtype: "Data",
				hidden: 1,
			},
		];

		return variant_fields;
	}
};
