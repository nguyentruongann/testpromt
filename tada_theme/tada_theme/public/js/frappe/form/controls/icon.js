frappe.ui.form.ControlIcon = class TadaControlIcon extends (
	frappe.ui.form.ControlIcon
) {
	get_all_icons() {
		frappe.symbols = [];
		$("#all-symbols > svg > symbol[id]").each(function () {
			this.id.includes("icon-") &&
				frappe.symbols.push(this.id.replace("icon-", ""));
		});
		$("#all-symbols > svg:nth-child(3) symbol[id]").each(function () {
			frappe.symbols.push(`lucide-${this.id}`);
		});
	}
};
