frappe.provide("frappe.ui.toolbar");

// TODO: Should be refactored later.
frappe.ui.toolbar.BranchSelector = class BranchSelector {
	constructor() {
		this.current_branch = frappe.defaults.get_user_default("branch");
		this.make();
	}

	make() {
		this.$el = $(`
            <div class="dropdown nav-item ml-0">
                <button class="btn btn-light btn-sm dropdown-toggle" data-toggle="dropdown" title="${__("Switch Branch")}">
                    <span class="branch-name small">${this.current_branch || __("Branch")}</span>
                </button>
                <div class="dropdown-menu dropdown-menu-right">
                    <div class="dropdown-header">${__("Select Branch")}</div>
                    <div class="branch-loading text-center py-2">
                        <i class="fa fa-spinner fa-spin text-muted"></i> ${__("Loading...")}
                    </div>
                </div>
            </div>
        `);
		$(".navbar").find(".dropdown-navbar-user").before(this.$el);
		this.$el
			.on("show.bs.dropdown", () => this.load_branches())
			.on("click", ".branch-item", (e) =>
				this.select($(e.currentTarget).data("branch")),
			);
	}

	load_branches() {
		frappe.db
			.get_list("Branch", {
				fields: ["name", "custom_company"],
				filters: { custom_disabled: 0 },
				order_by: "name asc",
				limit_page_length: 99999,
			})
			.then((branches) => {
				this.render(branches);
			});
	}

	render(branches) {
		const $menu = this.$el
			.find(".dropdown-menu")
			.empty()
			.append(`<div class="dropdown-header">${__("Select Branch")}</div>`);

		if (!branches.length)
			return $menu.append(
				`<div class="dropdown-item-text text-muted">${__("No branches found")}</div>`,
			);

		for (const branch of branches) {
			const active = this.current_branch === branch.name;
			$menu.append(`
                <a class="dropdown-item branch-item ${active ? "active" : ""}" data-branch="${branch.name}" href="#">
					<div class="branch-name">${branch.name}</div>
                </a>
            `);
		}
	}

	select(name) {
		if (!name) return;

		this.$el
			.find(".branch-name")
			.html(`<i class="fa fa-spinner fa-spin"></i> ${__("Loading...")}`);

		frappe.call({
			method:
				"inno_erp.inno_core.overrides.session_default_settings.session_default_settings.set_session_default_values",
			args: { default_values: { branch: name } },
			freeze: true,
			freeze_message: __("Changing Branch..."),
			callback: (r) => {
				if (r.message === "success") {
					this.current_branch = name;
					this.$el.find(".branch-name").text(name);
					frappe.show_alert({
						message: __("Branch changed to {0}", [name]),
						indicator: "green",
					});
					frappe.ui.toolbar.clear_cache();
				} else this.showError();
			},
			error: () => this.showError(),
		});
	}

	showError() {
		frappe.msgprint({
			title: __("Error"),
			message: __("Failed to change branch. Please try again."),
			indicator: "red",
		});
		this.$el
			.find(".branch-name")
			.text(this.current_branch || __("Select Branch"));
	}
};
