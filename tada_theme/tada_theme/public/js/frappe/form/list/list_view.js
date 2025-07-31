frappe.provide("frappe.views");

frappe.views.ListView = class TadaListView extends frappe.views.ListView {
    constructor(opts) {
        super(opts);
        this.SKIP_ACTIONS = [__("Customize")]
    }

    get_menu_items() {
        const items = super.get_menu_items();
        if (!frappe.boot.developer_mode) {
            return items.filter((item) => !this.SKIP_ACTIONS.includes(item.label));
        }
        return items;
    }
}