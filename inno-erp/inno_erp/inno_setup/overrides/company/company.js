frappe.ui.form.on("Company", {
	onload_post_render(frm) {
		const duplicate_dom = frm.page.standard_actions.find(
			'span[data-label="Duplicate"]',
		);
		if (duplicate_dom.length) {
			duplicate_dom.parent().parent().remove();
		}
	},
});
