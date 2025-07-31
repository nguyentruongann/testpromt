frappe.provide("frappe.search");
frappe.provide("frappe.tags");

frappe.search.AwesomeBar = class TadaAwesomeBar extends (
  frappe.search.AwesomeBar
) {
  build_options(txt) {
    const options = super.build_options(txt);
    if (!frappe.boot.developer_mode) {
      return options.filter(
        (option) =>
          option?.route &&
          !frappe.tada.utils.SKIP_DOCTYPES.includes(option?.route[1]) &&
          !option?.route[1]?.endsWith(frappe.tada.utils.SKIP_ENDWITH)
      );
    }
    return options;
  }
};
