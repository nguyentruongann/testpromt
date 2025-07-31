frappe.ui.form.on("Brand", {
	brand: (frm) => {
		if (frm.doc.brand.includes(" ")) {
			frm.set_value("custom_abbr", frappe.get_abbr(frm.doc.brand));
			return;
		}
		frm.set_value("custom_abbr", frm.doc.brand);
	},
});
