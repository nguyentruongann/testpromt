frappe.ui.form.on("POS Invoice", {
    custom_select_discount: function (frm) {
		console.log("custom_select_pricing_rule called");
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
});