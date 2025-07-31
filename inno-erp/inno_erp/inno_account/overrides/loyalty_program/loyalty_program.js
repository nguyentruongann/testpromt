//validate field Date Of Effect of table speccial day in loyalty program\
frappe.ui.form.on("Loyalty Program", {
	setup: function (frm) {
		frm.get_field("collection_rules").grid.sortable_setup_done = true;
	},
	onload: function (frm) {
		if (frm.is_new()) {
			frm.set_value("collection_rules", [
				{
					custom_rate: 1,
					custom_minimum_total_orders: 0,
					custom_minimum_total_amount: 0,
					custom_minimum_total_items: 0,
				},
			]);
		}
	},

	conversion_factor: function (frm) {
		if (frm.doc.conversion_factor <= 0) {
			frappe.model.set_value(frm.doctype, frm.name, "conversion_factor", 0);
			frappe.throw(__("Conversion factor cannot be negative or zero."));
		}
	},
});
frappe.ui.form.on("Loyalty Program Collection", {
	custom_rate: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		const base_tier = frm.doc.collection_rules[0];
		if (row == base_tier) {
			if (parseFloat(row.custom_rate) != 1) {
				frappe.model.set_value(cdt, cdn, "custom_rate", 1);
				frappe.throw(__("Rate of base tier must be 1!"));
			}
		} else {
			const base_cf = parseFloat(base_tier.collection_factor);
			const rate = parseFloat(row.custom_rate || 0);
			const new_cf = base_cf / rate;
			frappe.model.set_value(cdt, cdn, "collection_factor", new_cf);
		}
	},
	collection_factor: function (frm, cdt, cdn) {
		const row = locals[cdt][cdn];
		const base_tier = frm.doc.collection_rules[0];
		const default_cf = parseFloat(base_tier.collection_factor);
		if (row == base_tier) {
			const collection_rules = frm.doc.collection_rules || [];
			for (let cr of collection_rules) {
				if (cr == base_tier) {
					continue;
				}
				const rate = parseFloat(cr.custom_rate || 0);
				const new_cf = default_cf / rate;
				frappe.model.set_value(cr.doctype, cr.name, "collection_factor", new_cf);
			}
		}
	},
});
