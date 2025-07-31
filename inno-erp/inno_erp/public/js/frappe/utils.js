frappe.provide("inno.utils");

inno.utils = {
	clear_actions: (frm, btn_labels, group) => {
		if (!btn_labels || btn_labels.length === 0) {
			return;
		}

		for (const btn_label of btn_labels) {
			inno.utils.clear_action(frm, btn_label, group);
		}
	},
	clear_action: (frm, btn_label, group) => {
		if (group) {
			const btn_dom = frm.page.wrapper
				.find(`[data-label="${encodeURIComponent(group)}"]`)
				.find(`[data-label="${encodeURIComponent(btn_label)}"]`);
			frm.page.clear_action_of(btn_dom);
		}
		const btn_dom = frm.page.wrapper.find(`[data-label="${encodeURIComponent(btn_label)}"]`);
		frm.page.clear_action_of(btn_dom);
	},
};
