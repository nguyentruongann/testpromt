frappe.provide("inno.sales_invoice");

frappe.ui.form.on("Sales Invoice", {
	onload: (frm) => {
		if (frm.is_new()) {
			frappe.utils.set_branch_session(frm);
		}
		frm.fields_dict["custom_payoo_orders"].grid.cannot_add_rows = true;
	},

	refresh: (frm) => {
		if (frm.is_new()) {
			frm.set_value("due_date", frappe.datetime.nowdate());
		}

		setTimeout(() => {
			inno.utils.clear_actions(
				frm,
				[
					__("Payment"),
					__("Payment Request"),
					__("Invoice Discounting"),
					__("Dunning"),
					__("Maintenance Schedule"),
					__("Quality Inspection(s)"),
				],
				__("Create")
			);
			// Check if Create has no actions then delete it

			inno.utils.clear_actions(
				frm,
				[__("Timesheet"), __("Delivery Note"), __("Quotation")],
				__("Get Items From")
			);

			if (!frm.is_new() && frm.doc.docstatus === 0) {
				frm.page.clear_primary_action();
				// if (frm.doc.docstatus === 1 && !frm.doc.is_return && frm.doc.outstanding_amount >= 0) {
				frm.add_custom_button(
					__("Print Invoice"),
					function () {
						inno.sales_invoice.direct_print_with_settings(frm);
					},
					__("Preview")
				);
				frm.add_custom_button(
					__("Payment"),
					function () {
						inno.sales_invoice.open_payment_dialog(frm);
					},
					__("Create")
				);
			}
		}, 800);
	},

	discount_amount: function (frm) {
		const doc = frm.doc;
		if (doc.discount_amount > 0 || doc.additional_discount_percentage > 0) {
			frm.trigger("assign_additional_discount_account");
		} else {
			frm.set_value("additional_discount_account", "");
		}
	},
	assign_additional_discount_account: async function (frm) {
		const company_account = await frappe.db.get_value(
			"Company",
			frm.doc.company,
			"default_discount_account"
		);

		if (!company_account?.message?.default_discount_account) {
			frappe.msgprint(__("Please setting up Default Discount Account in Company"));
			return;
		}

		if (frm.doc.additional_discount_percentage > 0 || frm.doc.discount_amount > 0) {
			frm.set_value(
				"additional_discount_account",
				company_account.message.default_discount_account
			);
			frm.refresh_field("additional_discount_account");
		}
	},
	before_save: function (frm) {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Sales Invoice Item", item.name);
		}
	},

	custom_select_pricing_rule: function (frm) {
		frm.trigger("show_pricing_rule_dialog");
	},

	custom_coupon_code: async function (frm) {
		const coupon_code = frm.doc.custom_coupon_code;

		if (frm.__selected_pricing_rules) {
			for (const item_code of Object.keys(frm.__selected_pricing_rules)) {
				frm.__selected_pricing_rules[item_code].coupon_pricing_rule = null;
			}
		}
		if (!coupon_code) {
			frm.cscript.apply_pricing_rule_from_dialog();
			return;
		}

		frappe.call({
			method: "inno_erp.controller.pricing_rule.validate_coupon_code",
			args: {
				args: {
					coupon_code: coupon_code,
					company: frm.doc.company,
					customer: frm.doc.customer,
					currency: frm.doc.currency,
					conversion_rate: frm.doc.conversion_rate,
					price_list: frm.doc.selling_price_list,
					transaction_date: frm.doc.transaction_date,
					items: frm.doc.items.map((item) => ({
						item_code: item.item_code,
						qty: item.qty,
						price_list_rate: item.price_list_rate,
					})),
					total: frm.doc.total,
					total_qty: frm.doc.total_qty,
				},
			},
			freeze: true,
			callback: async function (r) {
				if (r.message.valid === false) {
					frm.set_value("custom_coupon_code", "");
					const errorMessage = r.message.message || "Invalid coupon.";
					frappe.show_alert({ message: errorMessage, indicator: "red" });
					frm.coupon_pricing_rule = null;
					if (frm.__selected_pricing_rules) {
						for (const item_code of Object.keys(frm.__selected_pricing_rules)) {
							frm.__selected_pricing_rules[item_code].coupon_pricing_rule = null;
						}
					}
					frm.cscript.apply_pricing_rule_from_dialog();
				} else {
					if (r.message.is_transaction_level) {
						frm.coupon_pricing_rule = r.message.pricing_rule;
						frappe.show_alert({
							message: "Transaction coupon applied successfully!",
							indicator: "green",
						});
						frm.cscript.apply_pricing_rule_from_dialog();
					} else {
						const applicableItems = new Set(r.message.applicable.item_codes);
						if (!frm.__selected_pricing_rules) {
							frm.__selected_pricing_rules = {};
						}

						for (const item of frm.doc.items) {
							if (!item.is_free_item) {
								if (!frm.__selected_pricing_rules[item.item_code]) {
									frm.__selected_pricing_rules[item.item_code] = {
										coupon_pricing_rule: null,
										pricing_rule: null,
									};
								}
								if (applicableItems.has(item.item_code)) {
									frm.__selected_pricing_rules[
										item.item_code
									].coupon_pricing_rule = r.message.pricing_rule;
								}
							}
						}

						frappe.show_alert({
							message: "Item coupon applied successfully!",
							indicator: "green",
						});
						frm.cscript.apply_pricing_rule_from_dialog();
					}
				}
			},
		});
	},
});
