// Relative Navbar
frappe.ui.toolbar.Toolbar = class extends frappe.ui.toolbar.Toolbar {
	constructor() {
		super();
		// Custom navbar for TADA THEME
		$("#navbar-breadcrumbs").remove();
		$("header.navbar[role='navigation'] .navbar-brand.navbar-home").remove();
		$("header.navbar[role='navigation'] form[role='search']").removeClass(
			"justify-content-end",
		);
		$(".main-section > .sticky-top")
			.removeClass("sticky-top")
			.addClass("position-relative")
			.css("z-index", "10");

		// TODO: Should be refactored later.
		if (frappe.defaults.get_user_default("branch") != null) {
			this.branch_selector = new frappe.ui.toolbar.BranchSelector();
		}
	}
};
