// biome-ignore lint/complexity/useLiteralKeys: <explanation>
frappe.listview_settings["Item"] = {
	add_fields: ["stock_uom", "has_variants", "disabled", "variant_of"],
	get_indicator: (doc) => {
		if (doc.disabled) {
			return [__("Disabled"), "grey", "disabled,=,Yes"];
		}
		if (doc.end_of_life && doc.end_of_life < frappe.datetime.get_today()) {
			return [__("Expired"), "grey", "end_of_life,<,Today"];
		}
		if (doc.has_variants) {
			return [__("Template"), "orange", "has_variants,=,Yes"];
		}
		if (doc.variant_of) {
			return [__("Variant"), "green", `variant_of,=,${doc.variant_of}`];
		}
	},
};
