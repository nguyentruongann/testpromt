frappe.provide("frappe.views");

const ITEM_LIST_DOCTYPES = ["Item", "Omni Item"];
const MAX_VARIANTS = 9999;

frappe.views.ItemListView = class extends frappe.views.ListView {
	// biome-ignore lint/complexity/noUselessConstructor: <explanation>
	constructor(opts) {
		super(opts);
	}

	refresh(refresh_header = false) {
		this.cache_variants = {};
		return super.refresh(refresh_header);
	}

	get_call_args(isDefault = false) {
		if (isDefault) {
			return super.get_call_args();
		}

		const args = this.get_args();

		if (ITEM_LIST_DOCTYPES.includes(this.doctype)) {
			args.order_by = "name asc, modified desc";
			if (args.filters.length === 0) {
				args.filters.push([this.doctype, "variant_of", "is", "not set"]);
			}
		}

		return {
			method: this.method,
			args: args,
			freeze: this.freeze_on_refresh || false,
			freeze_message: this.freeze_message || `${__("Loading")}...`,
		};
	}

	setup_list_click() {
		if (!ITEM_LIST_DOCTYPES.includes(this.doctype)) {
			super.setup_list_click();
			return;
		}

		this.$result.on("click", ".list-row, .image-view-header, .file-header", (e) => {
			const $target = $(e.target);
			// tick checkbox if Ctrl/Meta key is pressed
			if ((e.ctrlKey || e.metaKey) && !$target.is("a")) {
				const $list_row = $(e.currentTarget);
				const $check = $list_row.find(".list-row-checkbox");
				$check.prop("checked", !$check.prop("checked"));
				e.preventDefault();
				this.on_row_checked();
				return;
			}
			// don't open form when checkbox, like, filterable are clicked
			if (
				$target.hasClass("filterable") ||
				$target.hasClass("select-like") ||
				$target.hasClass("file-select") ||
				$target.hasClass("list-row-like") ||
				$target.is(":checkbox")
			) {
				e.stopPropagation();
				return;
			}

			// link, let the event be handled via set_route
			if ($target.is("a")) return;

			// WARN(inno): Custom code start from here
			const $list_row_dom = $target.closest(".list-row");
			const template_item = $list_row_dom.find(`a[data-doctype='${this.doctype}']`).data();
			const item_idx = this.data.findIndex((d) => d.name === `${template_item.name}`);

			if (this.data[item_idx]?.has_variants) {
				return this.toggle_variant_area(`${template_item.name}`, () => {
					window.scrollTo(0, window.scrollY);
				});
			}
			// END CUSTOM

			// clicked on the row, open form
			const $row = $(e.currentTarget);
			const link = $row.find(".list-subject a").get(0);
			if (link) {
				frappe.set_route(link.pathname);
				return false;
			}
		});
	}

	toggle_variant_area(template_name, callback) {
		const idx_after_template = this.data.findIndex((d) => d.name === template_name) + 1;
		if (
			idx_after_template < this.data.length &&
			this.data[idx_after_template].variant_of === template_name
		) {
			this.data = this.data.filter((d) => d.variant_of !== template_name);
			this.refresh_on_change_variant();
			return Promise.resolve().then(callback);
		}

		return this.get_variants_only(template_name).then(callback);
	}

	get_variants_only(template_name) {
		this.cache_variants = this.cache_variants || {};
		if (this.cache_variants[template_name]) {
			const idx_after_template = this.data.findIndex((d) => d.name === template_name) + 1;

			this.data.splice(idx_after_template, 0, ...this.cache_variants[template_name]);
			this.data = this.data.uniqBy((d) => d.name);
			this.refresh_on_change_variant();
			return Promise.resolve();
		}

		const args = this.get_call_args(true);

		if (ITEM_LIST_DOCTYPES.includes(this.doctype)) {
			args.args.filters = args.args.filters.filter(
				(f) => f[1] !== "has_variants" && f[1] !== "variant_of"
			);
			args.args.filters.push([this.doctype, "variant_of", "=", template_name]);
			args.args.page_length = MAX_VARIANTS;
		}

		this.freeze(true);
		// fetch data from server
		return frappe.call(args).then((r) => {
			this.prepare_data_variant(r, template_name);
			this.refresh_on_change_variant();
		});
	}

	refresh_on_change_variant() {
		this.toggle_result_area();
		this.before_render();
		this.render();
		this.after_render();
		this.freeze(false);
		this.reset_defaults();
		if (this.settings.refresh) {
			this.settings.refresh(this);
		}
	}

	prepare_data_variant(r, template_name) {
		let data = r.message || {};

		// extract user_info for assignments
		Object.assign(frappe.boot.user_info, data.user_info);
		// biome-ignore lint/performance/noDelete: <explanation>
		delete data.user_info;

		data = !Array.isArray(data) ? frappe.utils.dict(data.keys, data.values) : data;

		const idx_after_template = this.data.findIndex((d) => d.name === template_name) + 1;

		// Cache the variants
		this.cache_variants[template_name] = data;

		this.data.splice(idx_after_template, 0, ...data);

		this.data = this.data.uniqBy((d) => d.name);
	}

	get_list_row_html(doc) {
		return this.get_list_row_html_skeleton(
			doc,
			this.get_left_html(doc),
			this.get_right_html(doc)
		);
	}

	get_list_row_html_skeleton(doc, left = "", right = "") {
		const isVariant = doc.variant_of != null;
		let appendClass = isVariant ? "variant-row-container" : "";

		// Template row
		let isCollapsedTemplate = false;
		if (doc.has_variants) {
			const next_idx = doc._idx + 1;

			if (next_idx < this.data.length && this.data[next_idx].variant_of === doc.name) {
				isCollapsedTemplate = true;
			}
		}

		appendClass = isCollapsedTemplate ? `${appendClass} template-row-container` : appendClass;

		// Last variant
		if (isVariant) {
			const next_idx = doc._idx + 1;
			if (doc._idx === this.data.length - 1) {
				appendClass += " last-row";
			}

			if (next_idx < this.data.length && doc.variant_of !== this.data[next_idx].variant_of) {
				appendClass += " last-row";
			}
		}

		return `
			<div class="list-row-container ${appendClass}" tabindex="1">
				<div class="level list-row">
					<div class="level-left ellipsis">
						${left}
					</div>
					<div class="level-right text-muted ellipsis">
						${right}
					</div>
				</div>
				<div class="list-row-border"></div>
			</div>
		`;
	}
};
