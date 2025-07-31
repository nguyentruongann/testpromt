frappe.ui.form.ControlCascader = class ControlCascader extends frappe.ui.form.ControlData {
	static trigger_change_on_input_event = false;
	make_input() {
		const options = this.df.options || [];

		// State: current path (array of option objects)
		this.cascaderPath = [];
		this.cascaderOpen = false;

		// Helper to get options for a given path
		function getOptionsForPath(path) {
			let opts = options;
			for (const node of path) {
				const found = opts.find((o) => o.value === node.value);
				if (found && found.children) {
					opts = found.children;
				} else {
					return [];
				}
			}
			return opts;
		}

		// Helper to render columns
		const renderColumns = (path) => {
			let columns = [];
			let currentPath = [];
			let opts = options;
			while (true) {
				columns.push(opts);
				const last = path[currentPath.length];
				if (!last) break;
				const found = opts.find((o) => o.value === last.value);
				if (found && found.children) {
					currentPath.push(found);
					opts = found.children;
				} else {
					break;
				}
			}
			return columns;
		};

		// Helper to get label path
		const getLabelPath = (path) => path.map((o) => o.label).join(" / ");

		// Main template
		const template = `
			<div class="cascader-wrapper" style="position:relative;">
				<button type="button" class="btn btn-secondary cascader-trigger" style="width:100%;text-align:left; background-color: #fff !important; border: 1px solid #d1d8dd !important;">
					<span class="cascader-label" style="color:rgb(0, 0, 0) !important;">${__("Select Option")}</span>
					<span class="caret" style="float:right;"></span>
				</button>
				<div class="cascader-panel rounded" style="display:none;position:absolute;z-index:1051;top:100%;left:0;background:#fff;border:1px solid #ddd;box-shadow:0 6px 12px rgba(0,0,0,.175);padding:8px 0;min-width:220px;white-space:nowrap;">
				</div>
			</div>
		`;

		this.$list_wrapper = $(template);
		this.$list_wrapper.prependTo(this.input_area);
		this.$panel = this.$list_wrapper.find(".cascader-panel");
		this.$trigger = this.$list_wrapper.find(".cascader-trigger");
		this.$label = this.$list_wrapper.find(".cascader-label");

		// Render panel columns
		const renderPanel = () => {
			const columns = renderColumns(this.cascaderPath);
			let html = '<div style="display:flex;gap:0;">';
			columns.forEach((opts, colIdx) => {
				html +=
					'<ul class="cascader-col" style="list-style:none;margin:0;padding:0 8px;min-width:160px;max-height:240px;overflow:auto;border-right:1px solid #eee;">';
				opts.forEach((opt) => {
					const isActive =
						this.cascaderPath[colIdx] && this.cascaderPath[colIdx].value === opt.value;
					html += `<li class="cascader-option${
						isActive ? " active" : ""
					}" data-value="${encodeURIComponent(
						opt.value
					)}" style="padding:6px 12px;cursor:pointer;${
						isActive ? "background:#f5f5f5;" : ""
					}">${opt.label}${
						opt.children ? " <span style='float:right;'>&#9654;</span>" : ""
					}</li>`;
				});
				html += "</ul>";
			});
			html += "</div>";
			this.$panel.html(html);
		};

		// Open/close panel
		const openPanel = () => {
			this.cascaderOpen = true;
			this.$panel.show();
			renderPanel();
		};
		const closePanel = () => {
			this.cascaderOpen = false;
			this.$panel.hide();
		};

		// Update label
		const updateLabel = () => {
			if (this.cascaderPath.length) {
				this.$label.text(getLabelPath(this.cascaderPath));
			} else {
				this.$label.text(__("Select Option"));
			}
		};

		// Trigger click
		this.$trigger.on("click", (e) => {
			if (this.cascaderOpen) {
				closePanel();
			} else {
				openPanel();
			}
			e.preventDefault();
		});

		// Panel option click
		this.$panel.on("click", ".cascader-option", (e) => {
			const $opt = $(e.currentTarget);
			const value = decodeURIComponent($opt.data("value"));
			const colIdx = $opt.closest(".cascader-col").index();
			const columns = renderColumns(this.cascaderPath);
			const opts = columns[colIdx];
			const selected = opts.find((o) => o.value === value);
			// Update path
			this.cascaderPath = this.cascaderPath.slice(0, colIdx);
			this.cascaderPath.push(selected);
			if (!selected.children) {
				// Leaf node: set value and close
				this.set_value(this.cascaderPath.map((o) => o.value));
				renderPanel();
				updateLabel();
			} else {
				renderPanel();
				updateLabel();
			}
			e.stopPropagation();
		});

		// Click outside to close
		$(document).on("mousedown.cascader", (e) => {
			if (
				!this.$list_wrapper.is(e.target) &&
				this.$list_wrapper.has(e.target).length === 0
			) {
				closePanel();
			}
		});

		// Set initial value if any
		this.value = this.value || [];
		if (this.value.length) {
			// Find path from value
			let path = [];
			let opts = options;
			for (const v of this.value) {
				const found = opts.find((o) => o.value === v);
				if (found) {
					path.push(found);
					opts = found.children || [];
				} else {
					break;
				}
			}
			this.cascaderPath = path;
			updateLabel();
		}
	}

	set_input_attributes() {
		this.$list_wrapper
			.attr("data-fieldtype", this.df.fieldtype)
			.attr("data-fieldname", this.df.fieldname);

		this.set_status(this.get_placeholder_text());

		if (this.doctype) {
			this.$list_wrapper.attr("data-doctype", this.doctype);
		}
		if (this.df.input_css) {
			this.$list_wrapper.css(this.df.input_css);
		}
		if (this.df.input_class) {
			this.$list_wrapper.addClass(this.df.input_class);
		}
	}

	clear_all_selections() {
		this.values = [];
		this._selected_values = [];
		this.update_status();
		this.set_selectable_items(this._options);
		this.parse_validate_and_set_in_model("");
	}

	toggle_select_item($selectable_item) {
		$selectable_item.toggleClass("selected");
		let value = decodeURIComponent($selectable_item.data().value);

		if ($selectable_item.hasClass("selected")) {
			this.values = this.values.slice();
			this.values.push(value);
		} else {
			this.values = this.values.filter((val) => val !== value);
		}
		this.update_selected_values(value);
		this.parse_validate_and_set_in_model("");
		this.update_status();
	}

	set_value(value) {
		if (!value) return Promise.resolve();
		if (typeof value === "string") {
			value = [value];
		}
		this.values = value;
		this.values.forEach((value) => {
			this.update_selected_values(value);
		});
		this.parse_validate_and_set_in_model("");
		this.update_status();
		return Promise.resolve();
	}

	update_label() {
		if (this.cascaderPath.length) {
			const getLabelPath = (path) => path.map((o) => o.label).join(" / ");
			this.$label.text(getLabelPath(this.cascaderPath));
		} else {
			this.$label.text(__("Select Option"));
		}
	}

	update_selected_values(value) {
		this._selected_values = this._selected_values || [];
		if (!this._options) {
			return;
		}
		let option = this._options.find((opt) => opt.value === value);
		if (option) {
			if (this.values.includes(value)) {
				this._selected_values.push(option);
			} else {
				this._selected_values = this._selected_values.filter((opt) => opt.value !== value);
			}
		}
	}

	update_status() {
		let text;
		if (this.values.length === 0) {
			text = this.get_placeholder_text();
		} else if (this.values.length === 1) {
			let val = this.values[0];
			let option = this._options.find((opt) => opt.value === val);
			text = option ? option.label : val;
		} else {
			text = __("{0} values selected", [this.values.length]);
		}
		this.set_status(text);
	}

	get_placeholder_text() {
		return `<span class="text-extra-muted">${this.df.placeholder || ""}</span>`;
	}

	set_status(text) {
		this.$list_wrapper.find(".status-text").html(text);
	}

	set_options() {
		let promise = Promise.resolve();

		function process_options(options) {
			return options.map((option) => {
				if (typeof option === "string") {
					return {
						label: option,
						value: option,
					};
				}
				if (!option.label) {
					option.label = option.value;
				}
				return option;
			});
		}

		if (this.df.get_data) {
			let txt = this.$filter_input.val();
			let value = this.df.get_data(txt);
			if (!value) {
				this._options = [];
			} else if (value.then) {
				promise = value.then((options) => {
					this._options = process_options(options);
				});
			} else {
				this._options = process_options(value);
			}
		} else {
			this._options = process_options(this.df.options);
		}
		return promise;
	}

	set_selectable_items(options) {
		let html = options
			.map((option) => {
				let encoded_value = encodeURIComponent(option.value);
				let selected = this.values.includes(option.value) ? "selected" : "";
				return `<li class="selectable-item ${selected}" data-value="${encoded_value}">
				<div>
					<strong>${option.label}</strong>
					<div class="small">${option.description}</div>
				</div>
				<div class="multiselect-check">${frappe.utils.icon("tick", "xs")}</div>
			</li>`;
			})
			.join("");
		if (!html) {
			html = `<li class="text-muted">${__("No values to show")}</li>`;
		}
		this.$list_wrapper.find(".selectable-items").html(html);

		this.highlighted = -1;
	}

	get_value() {
		return this.values;
	}

	highlight_item(value) {
		this.highlighted += value;

		if (this.highlighted < 0) {
			this.highlighted = 0;
		}
		let $items = this.$list_wrapper.find(".selectable-item");
		if (this.highlighted > $items.length - 1) {
			this.highlighted = $items.length - 1;
		}

		let $item = $items[this.highlighted];

		if (this._$last_highlighted) {
			this._$last_highlighted.removeClass("highlighted");
		}
		this._$last_highlighted = $($item).addClass("highlighted");
		this.scroll_dropdown_if_needed($item);
	}

	scroll_dropdown_if_needed($item) {
		if ($item.scrollIntoView) {
			$item.scrollIntoView({ behavior: "smooth", block: "nearest", inline: "start" });
		} else {
			$item.parentNode.scrollTop = $item.offsetTop - $item.parentNode.offsetTop;
		}
	}
};

// Helper to find label by value in nested options
function findLabelByValue(options, value) {
	for (const opt of options) {
		if (opt.value === value) return opt.label;
		if (opt.children) {
			const found = findLabelByValue(opt.children, value);
			if (found) return found;
		}
	}
	return null;
}
