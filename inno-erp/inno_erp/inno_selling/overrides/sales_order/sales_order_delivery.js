frappe.provide("inno.sales_order");

inno.sales_order = {
	show_delivery_service_dialog: (frm) => {
		// Create dialog
		let dialog = new frappe.ui.Dialog({
			title: __("Delivery Service"),
			size: "extra-large",
			fields: [
				{
					fieldtype: "Section Break",
					label: __("Address"),
				},
				{
					fieldtype: "Phone",
					fieldname: "phone",
					label: __("Phone"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Column Break",
				},
				{
					fieldtype: "Data",
					fieldname: "address_line_1",
					label: __("Address"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Column Break",
				},
				{
					fieldtype: "Link",
					fieldname: "address_location",
					options: "Address Location",
					label: __("Address Location"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
						dialog.set_value("address_ward", "");
						dialog.set_df_property(
							"address_ward",
							"read_only",
							dialog.get_value("address_location") ? 0 : 1
						);
					},
				},
				{
					fieldtype: "Column Break",
				},
				{
					fieldtype: "Link",
					fieldname: "address_ward",
					options: "Address Ward",
					label: __("Address Ward"),
					read_only: 1,
					get_query() {
						return {
							filters: {
								location: dialog.get_value("address_location"), // Example filter based on the current form's document name
							},
						};
					},
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Section Break",
					label: __("Package"),
				},
				{
					fieldtype: "Float",
					fieldname: "package_length",
					label: __("Package Length (cm)"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Float",
					fieldname: "package_weight",
					label: __("Total Weight (Kg)"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Column Break",
				},
				{
					fieldtype: "Float",
					fieldname: "package_width",
					label: __("Package Width (cm)"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Currency",
					fieldname: "package_value",
					label: __("Package Value"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Column Break",
				},
				{
					fieldtype: "Float",
					fieldname: "package_height",
					label: __("Package Height (cm)"),
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Select",
					fieldname: "service_filter",
					label: __("Filter by Service Type"),
					options: "SAVING\nFAST\nEXPRESS",
					default: "SAVING",
					onchange: function () {
						inno.sales_order.calculate_delivery_fees(frm, dialog);
					},
				},
				{
					fieldtype: "Section Break",
				},
				{
					fieldtype: "HTML",
					fieldname: "delivery_options",
					options:
						'<div class="delivery-options-container"><div class="table-responsive"><table class="table table-bordered table-hover delivery-options-table"><thead><tr><th class="text-center d-none d-md-table-cell" style="width: 80px;">' +
						'</th><th class="d-none d-sm-table-cell">' +
						__("Provider") +
						"</th><th>" +
						__("Service") +
						'</th><th class="text-right">' +
						__("Price") +
						`</th></tr></thead><tbody><tr><td colspan="4" class="text-center"><span>${__(
							"Loading delivery rates..."
						)}</span></td></tr></tbody></table></div></div>`,
				},
			],
			primary_action_label: __("Create Order"),
			primary_action: function () {
				if (!dialog.selected_delivery_option) {
					frappe.msgprint(__("Please select a delivery service."));
					return;
				}
				if (!inno.sales_order.validate_required_fields(dialog, true)) {
					return;
				}

				inno.sales_order.create_delivery_order(
					frm,
					dialog.selected_delivery_option,
					dialog
				);
			},
			onload: function () {
				// Initialize dialog after rendering
				if (
					dialog.fields_dict.delivery_options &&
					dialog.fields_dict.delivery_options.wrapper
				) {
					$(dialog.fields_dict.delivery_options.wrapper).hide();
					// Disable row selection checkboxes
					if (dialog.fields_dict.delivery_options.grid) {
						dialog.fields_dict.delivery_options.grid.static_rows = true;
						dialog.fields_dict.delivery_options.grid.wrapper
							.find(".grid-row-check")
							.hide();
					}
				}
				// Store package details in dialog for API call
				dialog.package_details = {
					total_weight: total_weight,
					total_value: total_value,
					item_count: item_count,
				};
				inno.sales_order.calculate_delivery_fees(frm, dialog);
			},
		});

		// Store original data for filtering
		dialog.delivery_rates_data = [];

		dialog.show();

		// Load delivery rates immediately after showing dialog
		inno.sales_order.calculate_delivery_fees(frm, dialog);
	},

	populate_delivery_table: (frm, dialog, fee_data) => {
		// Get the HTML table container
		let table_container = $(dialog.fields_dict.delivery_options.wrapper).find(
			".delivery-options-table tbody"
		);

		if (table_container.length === 0) {
			console.error("Table container not found");
			return;
		}

		// Clear existing rows
		table_container.empty();

		fee_data.forEach((fee, index) => {
			let row_html = `
				<tr data-provider-key="${fee.provider}" data-index="${index}" class="delivery-option-row">
					<td class="text-center d-none d-md-table-cell">
						<input type="radio" name="delivery_option" value="${fee.provider}"
							class="delivery-option-radio" data-index="${index}">
					</td>
					<td class="d-none d-sm-table-cell provider-cell">${fee.provider}</td>
					<td class="service-cell">
						<div class="d-md-none mb-1">
							<input type="radio" name="delivery_option" value="${fee.provider}"
								class="delivery-option-radio me-2" data-index="${index}">
						</div>
						<div class="d-sm-none text-muted small">${fee.provider}</div>
						<div>${fee.service}</div>
					</td>
					<td class="text-right price-cell">${format_currency(fee.fee)}</td>
				</tr>
			`;

			table_container.append(row_html);
		});

		// Store rates data for later use
		dialog.delivery_rates_data = fee_data;

		// Add single selection logic
		inno.sales_order.setup_single_selection(dialog);
	},

	setup_single_selection: (dialog) => {
		// Handle radio button selection for HTML table
		$(dialog.fields_dict.delivery_options.wrapper).on(
			"change",
			'input[name="delivery_option"]',
			function () {
				let selected_key = $(this).val();
				let selected_index = $(this).data("index");

				// Store the selected option in dialog
				if (dialog.delivery_rates_data && dialog.delivery_rates_data[selected_index]) {
					dialog.selected_delivery_option = dialog.delivery_rates_data[selected_index];
				}

				// Highlight selected row
				$(dialog.fields_dict.delivery_options.wrapper)
					.find("tr")
					.removeClass("table-active");
				$(this).closest("tr").addClass("table-active");
			}
		);

		// Handle row click to select radio button
		$(dialog.fields_dict.delivery_options.wrapper).on("click", "tbody tr", function (e) {
			// Don't trigger if clicking directly on radio button
			if ($(e.target).is('input[type="radio"]')) {
				return;
			}

			// Click the radio button in this row
			$(this).find('input[type="radio"]').prop("checked", true).trigger("change");
		});
	},

	validate_required_fields: (dialog, require_all) => {
		let values = dialog.get_values();
		let required_fields = [
			"address_line_1",
			"address_location",
			"address_ward",
			"package_length",
			"package_width",
			"package_height",
			"package_weight",
			"package_value",
			"service_filter",
		];

		if (require_all == true) {
			required_fields.push("phone");
		}

		for (let field of required_fields) {
			if (!values[field]) {
				return false;
			}
		}

		return true;
	},

	calculate_delivery_fees: (frm, dialog) => {
		if (!inno.sales_order.validate_required_fields(dialog)) {
			return;
		}

		frappe.call({
			method: "inno_erp.inno_stock.overrides.delivery_note.delivery_note_utils.calculate_delivery_fees",
			args: {
				sales_order_name: frm.doc.name,
				...dialog.get_values(),
			},
			freeze: true,
			freeze_message: __("Calculating delivery fees..."),
			callback: function (r) {
				dialog.delivery_rates_data = r.message;

				// Populate table with new rates
				inno.sales_order.populate_delivery_table(frm, dialog, r.message);
			},
			error: function () {
				frappe.msgprint(__("Network error. Please check your connection and try again."));
			},
		});
	},

	create_delivery_order: (frm, selected_service, dialog) => {
		frappe.call({
			method: "inno_erp.inno_stock.overrides.delivery_note.delivery_note_utils.create_delivery_order",
			args: {
				selected_service,
				sales_order_name: frm.doc.name,
				...dialog.get_values(),
			},
			freeze: true,
			freeze_message: __("Creating delivery order..."),
			callback: function (r) {
				console.log(r);
				dialog.hide();
				dialog = null;
			},
			error: function () {
				frappe.msgprint(__("Network error. Please check your connection and try again."));
			},
		});
	},
};
