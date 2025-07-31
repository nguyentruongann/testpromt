frappe.provide("frappe.views");

frappe.views.ReportView = class TadaReportView extends frappe.views.ReportView {
    constructor(opts) {
        super(opts);

        // Overriding to hide sidebar by default
        !frappe.tada.utils.localHasKey("show_sidebar") && localStorage.setItem("show_sidebar", "false");
    }
}