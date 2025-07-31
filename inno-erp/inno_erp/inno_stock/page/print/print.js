frappe.provide("frappe.ui.form");

frappe.ui.form.PrintView = class InnoPrintView extends (
	frappe.ui.form.PrintView
) {
	// biome-ignore lint/complexity/noUselessConstructor: <explanation>
	constructor(opts) {
		super(opts);
	}

	setup_sidebar() {
		super.setup_sidebar();
		const route = frappe.get_route();
		const doctype = route[1];
		const print_view = this;
		if (doctype === "Item") {
			this.add_sidebar_item({
				fieldtype: "Select",
				fieldname: "page_type",
				label: __("Type/Size"),
				default: __("Choose Paper Pize"),
				options: [
					"",
					{
						label: __("Roll Decal - 3 labels - Size 104x22mm (4.2 x 0.9 Inch)"),
						value: 110,
					},
					{ label: __("Roll Decal - 2 labels - Size 72x22mm"), value: 78 },
					{ label: __("Roll Decal - 2 labels - Size 74x22mm"), value: 82 },
					{
						label: __("Roll Decal - 3 labels - Size Tomy 103 (202x162mm)"),
						value: 180,
					},
					{
						label: __("Roll Decal - 3 labels - Size Tomy 145 - A4"),
						value: 190,
					},
				],
				onchange: function () {
					// TODO(bao): should update doc normal way instead of using call an API
					frappe.call({
						method: "inno_erp.inno_stock.overrides.item.item.setup_barcode",
						args: {
							value: Number.parseInt(this.value),
							field: "custom_page_type",
							docname: frappe.get_route()[2],
						},
						callback: (r) => {
							print_view.preview();
							dialog.hide();
						},
					});
				},
			});
			this.add_sidebar_item({
				fieldtype: "Data",
				fieldname: "qty",
				placeholder: __("Amount to print"),
				onchange: function () {
					// TODO(bao): should update doc normal way instead of using call an API
					if (this.value) {
						frappe.call({
							method: "inno_erp.inno_stock.overrides.item.item.setup_barcode",
							args: {
								value: Number.parseInt(this.value),
								field: "custom_barcode_qty",
								docname: frappe.get_route()[2],
							},
							callback: (r) => {
								print_view.preview();
								dialog.hide();
							},
						});
					}
				},
			});
		}
	}
};
