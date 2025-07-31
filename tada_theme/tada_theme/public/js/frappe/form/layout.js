frappe.provide("frappe.ui.form");

frappe.ui.form.Layout = class TadaLayout extends frappe.ui.form.Layout {
	setup_events() {
		super.setup_events();
		const tabs_content = this.tabs_content[0];

		this.tab_link_container.off("click").on("click", ".nav-link", (e) => {
			e.preventDefault();
			e.stopImmediatePropagation();
			$(e.currentTarget).tab("show");
			if (tabs_content.getBoundingClientRect().top < 100) {
				tabs_content.scrollIntoView();
				setTimeout(() => {
					$(".form-tabs-list").removeClass("form-tabs-sticky-down");
					$(".form-tabs-list").addClass("form-tabs-sticky-up");
				}, 3);
			}
		});
	}
};
