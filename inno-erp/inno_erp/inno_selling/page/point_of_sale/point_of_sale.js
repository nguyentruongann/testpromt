frappe.provide("erpnext.PointOfSale");
frappe.provide("inno.PointOfSale");

frappe.pages["point-of-sale"].on_page_load = (wrapper) => {
	frappe.ui.make_app_page({
		parent: wrapper,
		title: __("Point of Sale"),
		single_column: true,
		disable_page_head: true,
	});

	frappe.require("point-of-sale.bundle.js", () => {
		inno.PointOfSale.override_pos_controller(wrapper);
		inno.PointOfSale.override_pos_item_selector();
		inno.PointOfSale.override_pos_item_cart();
		inno.PointOfSale.override_pos_payment();
		inno.PointOfSale.override_past_order_list();

		wrapper.pos = new erpnext.PointOfSale.Controller(wrapper);
		window.cur_pos = wrapper.pos;
	});
};

inno.PointOfSale.override_pos_controller = (wrapper) => {
	erpnext.PointOfSale.Controller = class extends (
		erpnext.PointOfSale.Controller
	) {
		constructor() {
			super(wrapper);
		}

		prepare_menu() {
			this.page.clear_menu();
		}

		init_item_selector() {
			super.init_item_selector();
			this.item_selector.events.toggle_recent_order = () =>
				this.toggle_recent_order();
			this.item_selector.events.close_pos = () => this.close_pos();
			this.item_selector.events.save_draft_invoice = () =>
				this.save_draft_invoice();
			this.item_selector.events.edit_draft_order = (name) =>
				this.edit_draft_order(name);
			this.item_selector.events.delete_draft_order = (name) =>
				this.delete_draft_order(name);
		}

		init_item_cart() {
			super.init_item_cart();
			this.cart.events.checkout = () => {
				this.save_and_checkout();
				if (!$.isEmptyObject(this.item_details.current_item)) {
					this.item_details.events.close_item_details();
				}
			};
		}

		save_draft_invoice() {
			if (!this.$components_wrapper.is(":visible")) return;

			if (this.frm.doc.items.length === 0) {
				frappe.show_alert({
					message: __("You must add atleast one item to save it as draft."),
					indicator: "red",
				});
				frappe.utils.play_sound("error");
				return;
			}

			this.frm
				.save(undefined, undefined, undefined, () => {
					frappe.show_alert({
						message: __("There was an error saving the document."),
						indicator: "red",
					});
					frappe.utils.play_sound("error");
				})
				.then(() => {
					frappe.run_serially([
						() => frappe.dom.freeze(),
						() => this.item_selector.refresh_draft_orders(),
						() => this.make_new_invoice(),
						() => frappe.dom.unfreeze(),
					]);
				});
		}

		edit_draft_order(invoice_name) {
			this.frm = this.get_new_frm(this.frm);
			this.frm.doc.items = [];
			frappe.db.get_doc("POS Invoice", invoice_name).then((invoice) => {
				frappe.run_serially([
					() => this.frm.refresh(invoice_name),
					() => this.frm.call("reset_mode_of_payments"),
					() => this.cart.load_invoice(),
					() => this.item_selector.toggle_component(true),
				]);
			});
		}

		delete_draft_order(invoice_name) {
			frappe.model.delete_doc(this.frm.doc.doctype, invoice_name, () => {
				this.item_selector.refresh_draft_orders();
			});
		}

		init_recent_order_list() {
			super.init_recent_order_list();
			this.recent_order_list.events.toggle_recent_order = () =>
				this.toggle_recent_order();
		}
	};
};

inno.PointOfSale.override_pos_item_selector = () => {
	erpnext.PointOfSale.ItemSelector = class extends (
		erpnext.PointOfSale.ItemSelector
	) {
		constructor({ frm, wrapper, events, pos_profile, settings }) {
			super({ frm, wrapper, events, pos_profile, settings });
		}

		prepare_dom() {
			super.prepare_dom();

			this.$component.find(".label").addClass("d-none");
			this.$component.find(".item-group-field").addClass("d-none");
			this.$component.find(".filter-section").append(`
				<div class="draft-order-wrapper">
					<div class="draft-order-list"></div>
				</div>
				<div class="pos-actions">
					<button type="button" class="btn btn-default icon-btn" data-toggle="dropdown" aria-expanded="false" aria-label="{{ __("Menu") }}">
						<span>
							<span class="menu-btn-group-label">
								<svg class="icon icon-sm">
									<use href="#icon-dot-horizontal">
									</use>
								</svg>
							</span>
						</span>
					</button>
					<ul class="dropdown-menu dropdown-menu-right" role="menu"></ul>
				</div>`);
			this.$draft_orders = this.$component.find(".draft-order-list");
			this.$pos_actions = this.$component.find(".pos-actions");

			this.render_actions();
			this.bind_action_events();
			this.refresh_draft_orders();
		}

		bind_action_events() {
			this.$draft_orders.on("click", ".draft-order", (e) => {
				e.stopPropagation();
				const invoice_name = unescape(
					$(e.currentTarget).attr("data-invoice-name"),
				);
				this.events.edit_draft_order(invoice_name);
			});

			this.$draft_orders.on("click", ".draft-order-remove", (e) => {
				e.stopPropagation();
				const $draft_order = $(e.currentTarget).parent();
				const invoice_name = unescape($draft_order.attr("data-invoice-name"));
				this.events.delete_draft_order(invoice_name);
			});
		}

		render_actions() {
			$(
				`<a class="dropdown-item" href="#" onclick="return false;" data-label="${encodeURIComponent(
					"Save Draft",
				)}">${__("Save Draft")}</a>`,
			)
				.on("click", () => this.events.save_draft_invoice())
				.appendTo(this.$pos_actions.find(".dropdown-menu"));

			$(
				`<a class="dropdown-item" href="#" onclick="return false;" data-label="${encodeURIComponent(
					"Recent Orders",
				)}">${__("Recent Orders")}</a>`,
			)
				.on("click", () => this.events.toggle_recent_order())
				.appendTo(this.$pos_actions.find(".dropdown-menu"));

			$(
				`<a class="dropdown-item" href="#" onclick="return false;" data-label="${encodeURIComponent(
					"Close the POS",
				)}">${__("Close the POS")}</a>`,
			)
				.on("click", () => this.events.close_pos())
				.appendTo(this.$pos_actions.find(".dropdown-menu"));
		}

		render_draft_order(order) {
			const order_number =
				order.name.split("-")[order.name.split("-").length - 1];
			this.$draft_orders.append(`
				<div class="draft-order" data-invoice-name="${escape(order.name)}">
					<div class="draft-order-name">
						${order_number}
					</div>
					<div class="draft-order-customer">
						${frappe.ellipsis(order.customer, 20)}
					</div>
					<span class="draft-order-remove">${frappe.utils.icon("close", "sm")}<span>
				</div>`);
		}

		refresh_draft_orders() {
			return frappe.call({
				method:
					"erpnext.selling.page.point_of_sale.point_of_sale.get_past_order_list",
				freeze: true,
				args: { search_term: "", status: "Draft" },
				callback: (response) => {
					this.$draft_orders.html("");
					for (const order of response.message) {
						this.render_draft_order(order);
					}
				},
			});
		}
	};
};

inno.PointOfSale.override_pos_payment = () => {
	erpnext.PointOfSale.Payment = class extends erpnext.PointOfSale.Payment {
		constructor({ events, wrapper }) {
			super({ events, wrapper });
		}

		init_component() {
			this.prepare_dom();
			// Do not init numpad
			// this.initialize_numpad();
			this.bind_events();
			this.attach_shortcuts();
		}
	};
};

inno.PointOfSale.override_past_order_list = () => {
	erpnext.PointOfSale.PastOrderList = class extends (
		erpnext.PointOfSale.PastOrderList
	) {
		constructor({ wrapper, events }) {
			super({ wrapper, events });
		}

		init_component() {
			super.init_component();

			this.$component.find(".label").replaceWith(`
				<div class="d-flex justify-content-between">
					<div class="label">${__("Recent Orders")}</div>
					<button class="btn icon-btn close-past-order-list">${frappe.utils.icon("close", "lg")}</button>
				</div>
			`);

			this.$component.find(".close-past-order-list").on("click", () => {
				this.events.toggle_recent_order();
			});
		}
	};
};

inno.PointOfSale.override_pos_item_cart = () => {
	erpnext.PointOfSale.ItemCart = class extends erpnext.PointOfSale.ItemCart {
		constructor({ wrapper, events, settings }) {
			super({ wrapper, events, settings });
		}

		init_cart_components() {
			super.init_cart_components();
			this.$component
				.find(".rate-amount-header")
				.before(`<div class="price-list-amount-header">Unit Price</div>`);
			this.$component
				.find(".rate-amount-header")
				.after(`<div class="action-header">&nbsp</div>`);
			this.$component.find(".numpad-section").addClass("d-none");
		}

		attach_shortcuts() {
			// Disable shortcuts
		}

		toggle_numpad(show) {
			// Do not use numpad anymore
		}

		update_customer_section() {
			super.update_customer_section();
			const {
				customer,
				email_id = "",
				mobile_no = "",
				image,
			} = this.customer_info || {};
			if (customer && this.customer_info.loyalty_points) {
				$(".customer-name-desc").after(
					`<div class=\"customer-desc\">Loyalty Point: <span class="text-success">${this.customer_info.loyalty_points}</span></div>`,
				);
			}
		}

		render_cart_item(item_data, $item_to_update) {
			const currency = this.events.get_frm().doc.currency;
			const me = this;

			if (!$item_to_update.length) {
				this.$cart_items_wrapper.append(
					`<div class="cart-item-wrapper" data-row-name="${escape(item_data.name)}"></div>
						<div class="seperator"></div>`,
				);
				$item_to_update = this.get_cart_item(item_data);
			}

			$item_to_update.html(
				`${get_item_image_html()}
					<div class="item-name-desc">
						<div class="item-name">
							${item_data.item_name}
						</div>
						${get_description_html()}
					</div>
					${get_rate_discount_html()}
					${render_remove_item_html()}`,
			);

			const columns = [
				{
					itemSelector: ".item-rate-amount",
					headerSelector: ".rate-amount-header",
				},
				{
					itemSelector: ".item-price-list-rate-amount",
					headerSelector: ".price-list-amount-header",
				},
				{
					itemSelector: ".item-actions",
					headerSelector: ".action-header",
				},
			];

			// Apply dynamic width to each column
			for (const column of columns) {
				set_dynamic_width(column.itemSelector, column.headerSelector);
			}
			function set_dynamic_width(itemSelector, headerSelector) {
				const items = Array.from(me.$cart_items_wrapper.find(itemSelector));

				// Reset widths
				me.$cart_header.find(headerSelector).css("width", "");
				me.$cart_items_wrapper.find(itemSelector).css("width", "");

				// Calculate maximum width
				let max_width = items.reduce((max_width, elm) => {
					return Math.max(max_width, $(elm).width());
				}, 0);

				// Add 1px buffer and apply width
				max_width += 1;
				if (max_width === 1) max_width = "";

				me.$cart_header.find(headerSelector).css("width", max_width);
				me.$cart_items_wrapper.find(itemSelector).css("width", max_width);
			}

			function get_rate_discount_html() {
				if (
					item_data.rate &&
					item_data.amount &&
					item_data.rate !== item_data.amount
				) {
					return `
							<div class="item-qty-rate">
								<div class="item-qty"><span>${item_data.qty || 0} ${item_data.uom}</span></div>
								<div class="item-price-list-rate-amount">
									<div class="item-amount">${format_currency(item_data.rate, currency)}</div>
									<div class="item-amount"><span class="text-danger" style="text-decoration: line-through;">${item_data.discount_percentage > 0 ? format_currency(item_data.price_list_rate, currency) : ""}
									</span></div>
								</div>
								<div class="item-rate-amount">
									<div class="item-rate">${format_currency(item_data.amount, currency)}</div>
								</div>
							</div>`;
				}

				return `
					<div class="item-qty-rate">
						<div class="item-qty"><span>${item_data.qty || 0} ${item_data.uom}</span></div>
						<div class="item-price-list-rate-amount">
							<div class="item-amount">
								${format_currency(item_data.rate, currency)}
							</div>
							<div class="item-amount">
								<span class="text-danger" style="text-decoration: line-through;">${item_data.discount_percentage > 0 ? format_currency(item_data.price_list_rate, currency) : ""}</span>
							</div>
						</div>
						<div class="item-rate-amount">
							<div class="item-rate">${format_currency(item_data.amount, currency)}</div>
						</div>
					</div>`;
			}

			function render_remove_item_html() {
				return `
						<div class="item-actions pl-1 pb-1">${frappe.utils.icon("delete", "sm")}</div>
					`;
			}

			function get_description_html() {
				if (item_data.description) {
					if (item_data.description.indexOf("<div>") !== -1) {
						try {
							item_data.description = $(item_data.description).text();
						} catch (error) {
							item_data.description = item_data.description
								.replace(/<div>/g, " ")
								.replace(/<\/div>/g, " ")
								.replace(/ +/g, " ");
						}
					}
					item_data.description = frappe.ellipsis(item_data.description, 45);
					return `<div class="item-desc">${item_data.description}</div>`;
				}
				return "";
			}

			function get_item_image_html() {
				const { image, item_name } = item_data;
				if (!me.hide_images && image) {
					return `
							<div class="item-image">
								<img
									onerror="cur_pos.cart.handle_broken_image(this)"
									src="${image}" alt="${frappe.get_abbr(item_name)}"">
							</div>`;
				}

				return `<div class="item-image item-abbr">${frappe.get_abbr(item_name)}</div>`;
			}
		}

		make_customer_selector() {
			this.$customer_section.html(`
				<div class="customer-field"></div>
			`);
			const me = this;
			const allowed_customer_group = this.allowed_customer_groups || [];
			// WARN(inno): Custom code start from here
			let filters = { is_internal_customer: 0 };
			// END CUSTOM CODE
			if (allowed_customer_group.length) {
				filters = {
					customer_group: ["in", allowed_customer_group],
				};
			}
			this.customer_field = frappe.ui.form.make_control({
				df: {
					label: __("Customer"),
					fieldtype: "Link",
					options: "Customer",
					placeholder: __("Search by customer name, phone, email."),
					get_query: () => ({
						filters,
					}),
					onchange: function () {
						if (this.value) {
							const frm = me.events.get_frm();
							frappe.dom.freeze();
							frappe.model.set_value(
								frm.doc.doctype,
								frm.doc.name,
								"customer",
								this.value,
							);
							frm.script_manager
								.trigger("customer", frm.doc.doctype, frm.doc.name)
								.then(() => {
									frappe.run_serially([
										() => me.fetch_customer_details(this.value),
										() => me.events.customer_details_updated(me.customer_info),
										() => me.update_customer_section(),
										() => me.update_totals_section(),
										() => frappe.dom.unfreeze(),
									]);
								});
						}
					},
				},
				parent: this.$customer_section.find(".customer-field"),
				render_input: true,
			});
			this.customer_field.toggle_label(false);
		}

		bind_events() {
			super.bind_events();
			const me = this;

			this.$cart_items_wrapper.on("click", ".item-actions", function (e) {
				// Remove item quickly
				e.stopPropagation();
				const $cart_item = $(this).parent();

				const item_row_name = unescape($cart_item.attr("data-row-name"));
				me.events.cart_item_clicked({ name: item_row_name });

				setImmediate(() => {
					me.events.numpad_event(undefined, "remove");
				});
			});
		}
	};
};
