frappe.provide("frappe.views.list_view");

const ITEM_LIST_DOCTYPES = ["Item", "Omni Item"];

frappe.views.ListFactory = class InnoListFactory extends frappe.views.ListFactory {
	make(route) {
		const doctype = route[1];

		// List / Gantt / Kanban / etc
		let view_name = frappe.utils.to_title_case(route[2] || "List");

		// WARN(inno): Custom code start from here
		if (ITEM_LIST_DOCTYPES.includes(doctype) && view_name === "List") {
			view_name = "ItemList";
		}
		// END CUSTOM CODE

		// File is a special view
		if (doctype === "File" && !["Report", "Dashboard"].includes(view_name)) {
			view_name = "File";
		}

		let view_class = frappe.views[`${view_name}View`];
		if (!view_class) view_class = frappe.views.ListView;

		if (view_class?.load_last_view?.() ?? false) {
			// view can have custom routing logic
			return;
		}

		frappe.provide(`frappe.views.list_view.${doctype}`);

		const hide_sidebar = view_class.no_sidebar || !frappe.boot.desk_settings.list_sidebar;

		frappe.views.list_view[this.page_name] = new view_class({
			doctype: doctype,
			parent: this.make_page(true, this.page_name, hide_sidebar),
		});

		this.set_cur_list();
	}
};
