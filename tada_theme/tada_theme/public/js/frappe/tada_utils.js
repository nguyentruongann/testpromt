frappe.provide("frappe.tada");

frappe.tada.utils = {
  SKIP_DOCTYPES: [
    "DocType",
    "Page",
    "Report",
    "Workspace",
    "Customize Form",
    "DocType Layout",
    "Webhook",
  ],
  SKIP_ENDWITH: ["Settings"],

  handleRouteSidebarLink(e) {
    e.preventDefault();
    const dom = $(this);

    // Lấy thông tin từ data-*
    let link_to = dom.data("link-to");
    let type = dom.data("type");
    let stats_filter = dom.data("stats-filter");
    stats_filter = stats_filter ? JSON.parse(stats_filter) : null;

    let doc_view = dom.data("doc-view");
    let kanban_board = dom.data("kanban-board");
    let is_query_report = dom.data("is-query-report");
    let url = dom.data("url");

    let route = frappe.utils.generate_route({
      name: link_to,
      type: type,
      doctype: type,
      is_query_report:
        is_query_report === "null" || is_query_report === "undefined"
          ? null
          : is_query_report,
      doc_view:
        doc_view === "null" || doc_view === "undefined" ? null : doc_view,
      kanban_board:
        kanban_board === "null" || kanban_board === "undefined"
          ? null
          : kanban_board,
    });

    let filters = frappe.utils.get_filter_from_json(stats_filter);
    if (type == "DocType" && filters) {
      frappe.route_options = filters;
    }

    if (e.ctrlKey || e.metaKey) {
      frappe.open_in_new_tab = true;
    }

    if (type == "URL") {
      if (frappe.open_in_new_tab) {
        window.open(url, "_blank");
        frappe.open_in_new_tab = false;
      } else {
        window.location.href = url;
      }
      return;
    }

    frappe.set_route(route);
  },
  localHasKey(key) {
    return localStorage.getItem(key) !== null;
  },
};
