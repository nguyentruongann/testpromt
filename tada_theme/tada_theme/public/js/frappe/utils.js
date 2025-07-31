frappe.provide("frappe.utils");

const to_lucide_map = {
	// list: "lucide-list",
	// add: "lucide-plus",
	// select: "lucide-chevrons-up-down",
	// "es-line-reload": "lucide-refresh-cw",
	// "es-small-close": "lucide-x",
};

Object.assign(frappe.utils, {
	icon(
		icon_name,
		size = "sm",
		icon_class = "",
		icon_style = "",
		svg_class = "",
	) {
		let size_class = "";
		const is_espresso = icon_name.startsWith("es-");
		if (icon_class.includes("dot-horizontal")) {
			console.log("icon_class", icon_class);
		}

		if (typeof size === "object") {
			icon_style += ` width: ${size.width}; height: ${size.height}`;
		} else {
			size_class = `icon-${size}`;
		}

		if (to_lucide_map[icon_name]) {
			icon_name = to_lucide_map[icon_name];
		}

		const is_lucide = icon_name.startsWith("lucide-");
		if (is_lucide) {
			icon_name = icon_name.replace("lucide-", "");
			return `<svg class="icon ${size_class ? size_class : ""}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<use class="${icon_class}" href="#${icon_name}"></use>
			</svg>`;
		}

		icon_name = is_espresso ? `#${icon_name}` : `#icon-${icon_name}`;
		return `<svg class="${
			is_espresso
				? icon_name.startsWith("es-solid")
					? "es-icon es-solid"
					: "es-icon es-line"
				: "icon"
		} ${svg_class} ${size_class}" style="${icon_style}" aria-hidden="true">
			<use class="${icon_class}" href="${icon_name}"></use>
		</svg>`;
	},
});
