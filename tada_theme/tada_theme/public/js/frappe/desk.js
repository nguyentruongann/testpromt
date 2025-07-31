const SIDEBAR_BREAKPOINT = 768;
const DESKTOP_SIDEBAR = "desktop";
const MOBILE_SIDEBAR = "mobile";

frappe.Application = class TadaApplication extends frappe.Application {
  constructor() {
    super();

    if (frappe.boot.setup_complete) {
      // Sidebar Parts
      this.renderSideBar();

      // Nếu resize cửa sổ, kiểm tra lại để cập nhật sidebar
      $(window).on("resize", () => {
        this.renderSideBar();
      });
    }
  }

  renderSideBar() {
    const newTypeOfSidebar =
      window.innerWidth < SIDEBAR_BREAKPOINT ? MOBILE_SIDEBAR : DESKTOP_SIDEBAR;

    if (newTypeOfSidebar === MOBILE_SIDEBAR && !this.sidebarMenuMobile) {
      this.sidebarMenuMobile = new frappe.tada.SidebarMenuMobile();
    }

    if (newTypeOfSidebar === DESKTOP_SIDEBAR && !this.sidebarMenu) {
      this.sidebarMenu = new frappe.tada.SidebarMenu();
    }

    if (newTypeOfSidebar !== this.currentTypeOfSidebar) {
      this.currentTypeOfSidebar = newTypeOfSidebar;
      if (this.currentTypeOfSidebar === MOBILE_SIDEBAR) {
        this.sidebarMenuMobile.renderSidebar();
        return;
      }
      this.sidebarMenu.renderSidebar();
    }
  }
};
