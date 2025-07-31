const extendedRouter = Object.create(frappe.router);
const skip_routes = ["Workspaces", ""];

extendedRouter.route = async function () {
	// resolve the route from the URL or hash
	// translate it so the objects are well defined
	// and render the page as required

	if (!frappe.app) return;

	const sub_path = this.get_sub_path();
	if (frappe.boot.setup_complete) {
		if (!frappe.re_route["setup-wizard"]) {
			frappe.re_route["setup-wizard"] = "app";
		}
	} else if (!sub_path.startsWith("setup-wizard")) {
		// biome-ignore lint/performance/noDelete: <explanation>
		frappe.re_route["setup-wizard"] && delete frappe.re_route["setup-wizard"];
		frappe.set_route(["setup-wizard"]);
	}
	if (this.re_route(sub_path)) return;

	this.current_sub_path = sub_path;
	this.current_route = await this.parse();

	////////////////////////////////////
	// Only changes within below code
	if (
		!frappe.boot.developer_mode &&
		(skip_routes.includes(this.current_route[0]) ||
			frappe.tada.utils.SKIP_DOCTYPES.includes(this.current_route[1]) ||
			this.current_route[1]?.endsWith(frappe.tada.utils.SKIP_ENDWITH))
	) {
		this.push_state("/app/dashboard-view/Selling");
		return;
	}
	////////////////////////////////////

	this.set_history(sub_path);
	this.render();
	this.set_title(sub_path);
	this.trigger("change");
};

frappe.router = extendedRouter;
