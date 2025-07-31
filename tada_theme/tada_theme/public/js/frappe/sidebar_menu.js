frappe.provide("frappe.tada");

const LOCAL_SIDEBAR_KEY = "_page:workspace_sidebar_items";
const USE_SHORTCUT_TYPES = ["shortcut", "header"];

frappe.tada.SidebarMenu = class TadaSidebarMenu {
  constructor() {
    $("body").prepend(frappe.render_template("sidebar_menu", {}));
  }

  renderSidebar() {
    $(".td-sidebar-menu-mobile").removeClass("d-none");
    $(".td-sidebar-menu-mobile, #sidebar-toggle").addClass("d-none");
    if (!$(".td-sidebar-menu nav > *").length) {
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
          USE_SHORTCUT_TYPES.includes(item.type)
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
            (shortcut) => shortcut.label === __(menu_item.data.shortcut_name)
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

          page.menu_items.push(header_map[header], ...menu_item_map[header]);
        }

        return page;
      });

    this.renderHTML();
  }

  // 🎯 Xử lý sidebar cho DESKTOP
  renderHTML() {
    const sidebar_wrapper = $(".td-sidebar-menu .nav");
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
						${idx === 0 ? "" : "<hr class='my-1'>"}
						<li class="nav-item mx-1" title="${shortcut.label}">
							<div class="p-2">
								<h5 class="font-weight-bold text-dark mb-0">${__(shortcut.label)}</h5>
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
						<span class="sidebar-item-label">${shortcut.label}</span>
						</a>
					</li>
				`;
        })
        .join("");

      sidebar_wrapper.append(
        $(`
			<li class="nav-item mx-1 has-submenu" id="page-${frappe.scrub(
        page.name
      )}" title="${page.label}">
				<a class="nav-link py-2 custom-submenu">
					<div class="mb-1">
						${frappe.utils.icon(page.icon, "md")}
					</div>
					<span class="title-label">${page.label}</span>
				</a>
			</li>
		`)
      );

      if (subMenuItems) {
        $(`#page-${frappe.scrub(page.name)}`).popover({
          container: "body",
          html: true,
          content: `<ul class="sidebar-submenu">${subMenuItems}</ul>`,
          trigger: "click",
          placement: "right",
          boundary: "viewport",
          delay: { show: 100, hide: 25 },
          sanitize: false,
          template: `<div class="popover sidebar-popover" role="tooltip">
						<div class="popover-body p-0"></div>
					</div>`,
        });
      }
    }
    this.setup_event_handler();
  }

  setup_event_handler() {
    // Handle popover events for better UX
    $(".nav-item.has-submenu")
      .on("mouseenter", function () {
        const $this = $(this);
        clearTimeout($this.data("hide-timer"));

        $this.popover("show");
      })
      .on("mouseleave", function () {
        const $this = $(this);
        const hideTimer = setTimeout(() => {
          $this.popover("hide");
        }, 100);
        $this.data("hide-timer", hideTimer);
      });

    // Keep popover open when hovering over it
    $(document)
      .on("mouseenter", ".sidebar-submenu", function () {
        const triggerId = $(this).parent().parent().attr("id");

        if (!triggerId) {
          return;
        }
        $(this).on(
          "click",
          ".nav-link",
          frappe.tada.utils.handleRouteSidebarLink
        );

        clearTimeout($(`[aria-describedby="${triggerId}"]`).data("hide-timer"));
      })
      .on("mouseleave", ".sidebar-submenu", function () {
        const triggerId = $(this).parent().parent().attr("id");
        if (!triggerId) {
          return;
        }
        $(`[aria-describedby="${triggerId}"]`).popover("hide");
      });
  }

  get_workspaces() {
    return frappe.xcall("frappe.desk.desktop.get_workspace_sidebar_items");
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
      "tada_theme.desk.desktop.get_workspace_sidebar_items"
    );
    localStorage.setItem(
      LOCAL_SIDEBAR_KEY,
      JSON.stringify({
        data: items,
        expires: new Date().getTime() + 300000, // 5 minutes
      })
    );
    return items;
  }
};
