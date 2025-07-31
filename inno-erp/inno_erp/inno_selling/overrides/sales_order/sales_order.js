frappe.provide("inno.sales_order");

frappe.ui.form.on("Sales Order", {
	refresh: (frm) => {
		if (frm.is_new()) {
			frm.set_value("delivery_date", frappe.datetime.nowdate());
			frappe.utils.set_branch_session(frm);
		}

		// Add delivery service selection button
		frm.trigger("add_delivery_service_button");
		frm.trigger("show_indicator_status");
	},

	onload_post_render: (frm) => {
		inno.utils.clear_actions(
			frm,
			[
				__("Pick List"),
				__("Work Order"),
				__("Material Request"),
				__("Request for Raw Materials"),
				__("Project"),
				__("Purchase Order"),
			],
			__("Create")
		);
	},

	show_indicator_status: (frm) => {
		frm.page.indicator.parent().find("#delivery-indicator").remove();
		frm.page.indicator.parent().find("#cod-indicator").remove();

		if (frm.doc.docstatus !== 1) {
			return;
		}

		frm.page.indicator.after(
			$(
				`<span id="delivery-indicator" class="ml-2 indicator-pill no-indicator-dot whitespace-nowrap ${frappe.utils.guess_colour(
					frm.doc.delivery_status
				)}">
					<span>${__(frm.doc.delivery_status)}</span>
				</span>`
			)
		);

		frm.page.indicator.after(
			$(
				`<span id="cod-indicator" class="ml-2 indicator-pill no-indicator-dot whitespace-nowrap ${"orange"}">
					<span>${"No COD"}</span>
				</span>`
			)
		);
	},

	after_submit: (frm) => {
		frm.refresh_fields();
	},

	before_save: (frm) => {
		for (const item of frm.doc.items) {
			frappe.utils.set_branch_cost_center_for_item(frm, "Sales Order Item", item.name);
		}
	},

	custom_select_pricing_rule: function (frm) {
		frm.trigger("show_pricing_rule_dialog");
	},

	coupon_code: async function (frm) {
		const coupon_code = frm.doc.coupon_code;

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
					frm.set_value("coupon_code", "");
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

	add_delivery_service_button: (frm) => {
		// Only show button for submitted sales orders that can create delivery notes
		if (
			frm.doc.docstatus === 1 &&
			frm.doc.status !== "Closed" &&
			frm.doc.delivery_status !== "Fully Delivered"
		) {
			frm.add_custom_button(
				__("Delivery"),
				function () {
					inno.sales_order.show_delivery_service_dialog(frm);
				},
				__("Create")
			);
		}
	},

	onload: function (frm) {
		frm.redemption_conversion_factor = null;
	},

	custom_redeem_loyalty_points: function (frm) {
		frm.trigger("get_loyalty_details");
	},

	get_loyalty_details: function (frm) {
		if (frm.doc.customer && frm.doc.redeem_loyalty_points) {
			frappe.call({
				method: "erpnext.accounts.doctype.loyalty_program.loyalty_program.get_loyalty_program_details",
				args: {
					customer: frm.doc.customer,
					loyalty_program: frm.doc.custom_loyalty_program,
					expiry_date: frm.doc.transaction_date,
					company: frm.doc.company,
				},
				callback: function (r) {
					if (r) {
						frm.set_value(
							"custom_loyalty_redemption_account",
							r.message.expense_account
						);
						frm.set_value(
							"custom_loyalty_redemption_cost_center",
							r.message.cost_center
						);
						frm.redemption_conversion_factor = r.message.conversion_factor;
					}
				},
			});
		}
	},

	set_loyalty_points: function (frm) {
		if (frm.redemption_conversion_factor) {
			let loyalty_amount = flt(
				frm.redemption_conversion_factor * flt(frm.doc.loyalty_points),
				precision("loyalty_amount")
			);
			var remaining_amount = flt(frm.doc.grand_total) - flt(frm.doc.advance_paid);
			if (frm.doc.grand_total && remaining_amount < loyalty_amount) {
				let redeemable_points = parseInt(
					remaining_amount / frm.redemption_conversion_factor
				);
				frappe.throw(
					__("You can only redeem max {0} points in this order.", [redeemable_points])
				);
			}
			frm.set_value("loyalty_amount", loyalty_amount);
		}
	},

	loyalty_points: function (frm) {
		if (frm.redemption_conversion_factor) {
			frm.events.set_loyalty_points(frm);
		} else {
			frappe.call({
				method: "erpnext.accounts.doctype.loyalty_program.loyalty_program.get_redeemption_factor",
				args: {
					loyalty_program: frm.doc.custom_loyalty_program,
				},
				callback: function (r) {
					if (r) {
						frm.redemption_conversion_factor = r.message;
						frm.events.set_loyalty_points(frm);
					}
				},
			});
		}
	},

	calculate_outstanding_amount_sales_order(frm) {
		if (frm.doc.is_return || frm.doc.docstatus > 0) return;

		frappe.model.round_floats_in(frm.doc, ["grand_total", "advance_paid", "loyalty_amount"]);

		let grand_total = frm.doc.rounded_total || frm.doc.grand_total;
		let base_grand_total = frm.doc.base_rounded_total || frm.doc.base_grand_total;

		let total_amount_to_pay;
		if (frm.doc.party_account_currency === frm.doc.currency) {
			total_amount_to_pay = flt(
				grand_total - frm.doc.advance_paid,
				precision("grand_total")
			);
		} else {
			total_amount_to_pay = flt(
				flt(base_grand_total, precision("base_grand_total")) - frm.doc.advance_paid,
				precision("base_grand_total")
			);
		}

		if (frm.doc.custom_redeem_loyalty_points && frm.doc.loyalty_amount) {
			total_amount_to_pay = flt(
				total_amount_to_pay - frm.doc.loyalty_amount,
				precision("grand_total")
			);
		}

		frm.doc.custom_outstanding_amount = flt(
			total_amount_to_pay,
			precision("custom_outstanding_amount")
		);

		if (frm.refresh_field) {
			frm.refresh_field("custom_outstanding_amount");
		}
	},

	loyalty_amount(frm) {
		frm.trigger("calculate_outstanding_amount_sales_order");
		frm.refresh_field("custom_outstanding_amount");
	},
});
