frappe.query_reports["Cash Book"] = {
	filters: [
		{
			fieldname: "company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1,
			hidden: 1,
		},
		{
			fieldname: "from_date",
			label: __("From Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_start(),
			reqd: 1,
		},
		{
			fieldname: "to_date",
			label: __("To Date"),
			fieldtype: "Date",
			default: frappe.datetime.month_end(),
			reqd: 1,
		},
		// {
		// 	fieldname: "mode_of_payments",
		// 	label: __("Mode of Payment"),
		// 	fieldtype: "MultiSelectList",
		// 	get_data: function (txt) {
		// 		// return frappe.db.get_link_options("Mode of Payment", txt);
		// 		let mode_of_payments = frappe.query_report.get_filter_value("mode_of_payments");
		// 		console.log(mode_of_payments);
		// 		if (!mode_of_payments) return;

		// 		return frappe.db.get_link_options(mode_of_payments, txt);
		// 	},
		// },
		{
			fieldname: "payment_types",
			label: __("Payment Type"),
			fieldtype: "MultiSelectList",
			get_data: function (txt) {
				return [
					{ value: "Receive", label: __("Receive"), description: "" },
					{ value: "Pay", label: __("Pay"), description: "" },
				];
			},
		},
		{
			fieldname: "chart",
			label: __("Chart"),
			fieldtype: "Select",
			options: [
				{
					value: "cash_flow_trend",
					label: __("Cash Flow Trend (Line)"),
				},
				{ value: "balance_trend", label: __("Balance (Line)") },
				{
					value: "income_expense_comparison",
					label: __("Income vs Expense (Bar)"),
				},
				{
					value: "daily_bar_comparison",
					label: __("Daily Net Flow (Bar)"),
				},
				{ value: "weekly_summary", label: __("Weekly Summary (Bar)") },
			],
			default: "cash_flow_trend",
		},
	],
	formatter: function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);

		if (!data) return value;

		const COLOR_PALLETE = {
			receive: "var(--green-600)",
			pay: "var(--red-600)",
			transfer: "var(--blue-600)",
			income: "var(--green-600)",
			expense: "var(--red-600)",
		};

		const applyStyle = (text, color, weight = 500) =>
			`<span style='color:${color}; font-weight: ${weight};'>${text}</span>`;

		const COLUMNS = {
			payment_type: "payment_type",
			income: "income",
			expense: "expense",
		};

		switch (column.fieldname) {
			case COLUMNS.payment_type:
				if (!data.payment_type) {
					break;
				}

				const paymentColors = {
					Receive: COLOR_PALLETE.receive,
					Pay: COLOR_PALLETE.pay,
					"Internal Transfer": COLOR_PALLETE.transfer,
				};

				const paymentColor = paymentColors[data.payment_type];
				if (paymentColor) {
					return applyStyle(data.payment_type, paymentColor);
				}
				break;
			case COLUMNS.income:
				return applyStyle(value, COLOR_PALLETE.income);
			case COLUMNS.expense:
				return applyStyle(value, COLOR_PALLETE.expense);
		}

		return value;
	},

	onload: function (report) {
		$("<style>")
			.prop("type", "text/css")
			.html(
				`
            .report-summary {
                justify-content: flex-end !important;
                background: #ffffff !important;
            }

            .report-summary .summary-label {
                text-transform: uppercase !important;
                font-weight: bold !important;
            }
            `
			)
			.appendTo("head");
	},
};
