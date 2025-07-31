frappe.provide("frappe.tada");

const LOCAL_SIDEBAR_KEY = "_page:workspace_sidebar_items";
const USE_SHORTCUT_TYPES = ["shortcut", "header"];

frappe.tada.SidebarMenuMobile = class TadaSidebarMenuMobile {
	constructor() {
		// Chờ DOM tải xong rồi tạo sidebar
		$("body").prepend(frappe.render_template("sidebar_menu_mobile", {}));
		$("body").prepend(
			`<button id="sidebar-toggle" class="mobile-menu-btn">☰</button>`,
		);

		$("#sidebar-toggle").on("click", (e) => {
			e.stopPropagation();
			this.toggleSidebarMobile();
		});
	}

	renderSidebar() {
		this.sidebar_dom = $(".td-sidebar-menu-mobile");
		this.sidebar_btn_dom = $("#sidebar-toggle");

		this.sidebar_dom.removeClass("d-none");
		this.sidebar_btn_dom.removeClass("d-none");

		if (!$(".td-sidebar-menu-mobile nav > *").length) {
			this.setup_pages();
			return;
		}
	}

	async setup_pages() {
		this.sidebar_pages =
			this.sidebar_pages ||
			this.get_cached_pages() ||
			(await this.get_pages_then_cache());

		this.all_pages = this.sidebar_pages.pages
			.filter((page) => page.is_hidden === 0)
			.map((page) => {
				const content = JSON.parse(page.content).filter((item) =>
					USE_SHORTCUT_TYPES.includes(item.type),
				);

				const header_map = {};
				const menu_item_map = {};

				let header_title = "DEFAULT";
				for (const menu_item of content) {
					if (menu_item.type === "header") {
						header_title = menu_item.data.text;
						header_map[header_title] = {
							label: __($(header_title).text()),
							type: "Header",
						};
						continue;
					}

					const shortcut = page.shortcuts.find(
						(shortcut) =>
							shortcut.label === __(menu_item.data.shortcut_name),
					);

					if (shortcut == null) continue;

					if (menu_item_map[header_title] == null) {
						menu_item_map[header_title] = [];
					}

					menu_item_map[header_title].push({
						...menu_item,
						...shortcut,
					});
				}

				let isFirstSection = true;
				page.menu_items = [];
				for (const header in header_map) {
					if (
						menu_item_map[header] == null ||
						menu_item_map[header].length === 0
					)
						continue;

					// TODO: temp fix
					if (
						isFirstSection &&
						menu_item_map[header].length === 1 &&
						menu_item_map[header][0].label === "Dashboard"
					) {
						isFirstSection = false;
						continue;
					}
					page.menu_items.push(
						header_map[header],
						...menu_item_map[header],
					);
				}

				return page;
			});

		this.renderHTML();
	}

	// 🎯 Xử lý sidebar cho MOBILE
	renderHTML() {
		const sidebar_wrapper = $(".td-sidebar-menu-mobile .nav");
		sidebar_wrapper.empty();

		for (const page of this.all_pages) {
			// TODO: temp fix
			if (page?.menu_items.length === 0) {
				continue;
			}

			const subMenuItems = page?.menu_items
				?.map((shortcut, idx) => {
					if (shortcut.type === "Header") {
						return `
							<li class="nav-item mx-1" title="${shortcut.label}">
								<div class="nav-link py-1">
								<h5 class="font-weight-bold text-white mb-0">${__(shortcut.label)}</h5>
								</div>
							</li>
						`;
					}
					return `
						<li>
							<a class="nav-link d-flex ml-3 sidebar-link"
							data-link-to="${shortcut.link_to || null}"
							data-type="${shortcut.type || null}"
							data-is-query-report="${shortcut.is_query_report || null}"
							data-doc-view="${shortcut.doc_view || null}"
							data-kanban-board="${shortcut.kanban_board}"
							data-url="${shortcut.url}"
							data-stats-filter='${JSON.stringify(shortcut.stats_filter)}'
							href="javascript:void(0);">
							<span class="sidebar-item-label text-white">${shortcut.label}</span>
							</a>
						</li>
					`;
				})
				.join("");

			const subMenu =
				subMenuItems.length > 0
					? `
						<ul class="sidebar-mobile-submenu">
						${subMenuItems}
						</ul>
					`
					: "";

			if (subMenu) {
				sidebar_wrapper.append(
					$(`
						<li class="nav-item mx-1 has-submenu" title="${page.label}">
							<a class="nav-link py-2 text-white custom-submenu">
							<div class="mb-1">
								${frappe.utils.icon(page.icon, "md")}
								<span class="title-label">${page.label}</span>
							</div>
							</a>
							${subMenu}
						</li>
					`),
				);
			}
		}

		$(".nav-item").click(function (e) {
			e.preventDefault();

			let parent = $(this);

			if (parent.hasClass("open")) {
				parent.removeClass("open");
				parent.find(".sidebar-mobile-submenu").slideUp();
			} else {
				$(".nav-item").removeClass("open"); // Đóng các menu khác
				$(".sidebar-mobile-submenu").slideUp();
				parent.addClass("open");
				parent.find(".sidebar-mobile-submenu").slideDown();
			}
		});

		const that = this;
		this.sidebar_dom
			.find(".sidebar-mobile-submenu .nav-link.sidebar-link")
			.on("click", function (e) {
				e.stopPropagation();
				frappe.tada.utils.handleRouteSidebarLink.bind(this)(e);
				that.toggleSidebarMobile();
			});

		this.sidebar_dom
			.find(".sidebar-mobile-card-submenu a.nav-link")
			.on("click", (e) => {
				this.toggleSidebarMobile();
			});
	}

	toggleSidebarMobile() {
		this.sidebar_dom.toggleClass("open");
		$("body").toggleClass("overflow-hidden");

		const isOpened = this.sidebar_dom.hasClass("open");
		if (isOpened) {
			this.sidebar_btn_dom.html("✖"); // Đổi thành dấu X
		} else {
			this.sidebar_btn_dom.html("☰"); // Đổi về icon menu
		}
	}

	async get_workspaces() {
		return await frappe.xcall(
			"frappe.desk.desktop.get_workspace_sidebar_items",
		);
	}

	get_cached_pages() {
		const cacheData = JSON.parse(localStorage.getItem(LOCAL_SIDEBAR_KEY));
		if (cacheData) {
			return cacheData.data;
		}

		return null;
	}

	async get_pages_then_cache() {
		const items = await frappe.xcall(
			"tada_theme.desk.desktop.get_workspace_sidebar_items",
		);
		localStorage.setItem(
			LOCAL_SIDEBAR_KEY,
			JSON.stringify({
				data: items,
				expires: new Date().getTime() + 300000, // 5 minutes
			}),
		);
		return items;
	}
};
