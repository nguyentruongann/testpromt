const td_global_filters = ["printer"];

frappe.ui.Page = class TadaPage extends frappe.ui.Page {
	constructor(opts) {
		super(opts);

		if (this.disable_page_head) {
			this.wrapper.find(".page-head").addClass("d-none");
		}
	}

	setup_sidebar_toggle() {
		// Do not use default sidebar, removing it by default.
		const sidebar_toggle = $(".page-head").find(".sidebar-toggle-btn");
		if (sidebar_toggle.length) {
			sidebar_toggle.remove();
		}
		if (this.disable_sidebar_toggle) {
			sidebar_toggle.last().remove();
			this.wrapper.addClass("no-list-sidebar");
		}
	}

	add_action_icon(icon, click, css_class = "", tooltip_label) {
		if (td_global_filters.includes(icon)) {
			return;
		}
		return super.add_action_icon(icon, click, css_class, tooltip_label);
	}

	setup_scroll_handler() {
		$(".page-head").css("top", "0px");

		$(window).scroll(
			frappe.utils.throttle(() => {
				$(".page-head").toggleClass(
					"drop-shadow",
					!!document.documentElement.scrollTop,
				);
			}, 500),
		);
	}
};
