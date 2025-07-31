// Copyright (c) 2025, Tada Labs and contributors
// For license information, please see license.txt
frappe.provide("inno.omni_item");

frappe.ui.form.on("Omni Item", {
	refresh(frm) {
		frm.trigger("display_omni_shop");
		frm.trigger("create_category_select");
		inno.omni_item.toggle_attributes(frm);
		inno.omni_item.add_creation_dialogs(frm);

		if (frm.doc.item_code && frm.doc.has_variants) {
			frm.page.set_indicator(__("Template"), "orange");
		} else if (frm.doc.item_code && frm.doc.variant_of) {
			frm.page.set_indicator(__("Variant"), "green");
		}

		frm.set_query("specification_template", (doc) => ({
			filters: {
				item_group: doc.item_group,
			},
		}));
	},
	has_variants(frm) {
		inno.omni_item.toggle_attributes(frm);
	},
	platform(frm) {
		frm.trigger("display_omni_shop");
	},
	display_omni_shop(frm) {
		const doc = frm.doc;
		if (doc.platform == "Website") {
			frm.set_df_property("shop", "hidden", true);
			frm.doc.shop = null;
			return;
		}

		frm.set_df_property("shop", "hidden", false);
		frm.set_query("shop", (doc) => ({
			filters: {
				platform: doc.platform,
			},
		}));
	},
	create_category_select(frm) {
		if (frm.category_dom) {
			frm.category_dom.destroy();
			frm.category_dom = null;
		}
		if (frm.fields_dict.category_html && frm.fields_dict.category_html.wrapper) {
			$(frm.fields_dict.category_html.wrapper).empty();
		}

		frm.category_area = frm.fields_dict.category_html.wrapper;
		frm.category_dom = new inno.omni_item.OmniCategorySelect(frm.category_area, frm);
	},

	specification_template: (frm) => {
		spec_template = frm.doc.specification_template;
		if (!spec_template) {
			return;
		}
		frappe.call({
			method: "frappe.client.get",
			args: {
				doctype: "Specification Template",
				name: frm.doc.specification_template,
			},
			callback: (r) => {
				if (r.message) {
					frm.clear_table("item_specifications");
					$.each(r.message.spec_item || [], (index, spec) => {
						const row = frm.add_child("item_specifications");
						row.spec_name = spec.spec_name;
						row.spec_value = spec.value;
					});
					frm.refresh_field("item_specifications");
				}
			},
		});
	},
});

$.extend(inno.omni_item, {
	add_creation_dialogs(frm) {
		if (frm.doc.has_variants) {
			frm.fields_dict["attributes"].grid.set_column_disp("attribute_value", false);
			if (frm.doc.variant_based_on === "Item Attribute") {
				frm.add_custom_button(
					__("Single Variant"),
					function () {
						inno.omni_item.show_single_variant_dialog(frm);
					},
					__("Create")
				);
				frm.add_custom_button(
					__("Multiple Variants"),
					function () {
						inno.omni_item.show_multiple_variants_dialog(frm);
					},
					__("Create")
				);
			}
		}
	},
	show_multiple_variants_dialog: function (frm) {
		var me = this;

		let promises = [];
		let attr_val_fields = {};

		function make_fields_from_attribute_values(attr_dict) {
			let fields = [];
			Object.keys(attr_dict).forEach((name, i) => {
				if (i % 3 === 0) {
					fields.push({ fieldtype: "Section Break" });
				}
				fields.push({ fieldtype: "Column Break", label: name });
				attr_dict[name].forEach((value) => {
					fields.push({
						fieldtype: "Check",
						label: value,
						fieldname: value,
						default: 0,
						onchange: function () {
							let selected_attributes = get_selected_attributes();
							let lengths = [];
							Object.keys(selected_attributes).map((key) => {
								lengths.push(selected_attributes[key].length);
							});
							if (lengths.includes(0)) {
								me.multiple_variant_dialog
									.get_primary_btn()
									.html(__("Create Variants"));
								me.multiple_variant_dialog.disable_primary_action();
							} else {
								let no_of_combinations = lengths.reduce((a, b) => a * b, 1);
								let msg;
								if (no_of_combinations === 1) {
									msg = __("Make {0} Variant", [no_of_combinations]);
								} else {
									msg = __("Make {0} Variants", [no_of_combinations]);
								}
								me.multiple_variant_dialog.get_primary_btn().html(msg);
								me.multiple_variant_dialog.enable_primary_action();
							}
						},
					});
				});
			});
			return fields;
		}

		function make_and_show_dialog(fields) {
			me.multiple_variant_dialog = new frappe.ui.Dialog({
				title: __("Select Attribute Values"),
				fields: [
					frm.doc.image
						? {
								fieldtype: "Check",
								label: __("Create a variant with the template image."),
								fieldname: "use_template_image",
								default: 0,
						  }
						: null,
					{
						fieldtype: "HTML",
						fieldname: "help",
						options: `<label class="control-label">
							${__("Select at least one value from each of the attributes.")}
						</label>`,
					},
				]
					.concat(fields)
					.filter(Boolean),
			});

			me.multiple_variant_dialog.set_primary_action(__("Create Variants"), () => {
				let selected_attributes = get_selected_attributes();
				let use_template_image =
					me.multiple_variant_dialog.get_value("use_template_image");

				me.multiple_variant_dialog.hide();

				frappe.call({
					method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.enqueue_multiple_variant_creation",
					args: {
						item: frm.doc.name,
						args: selected_attributes,
						use_template_image: use_template_image,
					},
					callback: function (r) {
						if (r.message === "queued") {
							frappe.show_alert({
								message: __("Variant creation has been queued."),
								indicator: "orange",
							});
						} else {
							frappe.show_alert({
								message: __("{0} variants created.", [r.message]),
								indicator: "green",
							});
						}
					},
				});
			});

			$(
				$(me.multiple_variant_dialog.$wrapper.find(".form-column")).find(".frappe-control")
			).css("margin-bottom", "0px");

			me.multiple_variant_dialog.disable_primary_action();
			me.multiple_variant_dialog.clear();
			me.multiple_variant_dialog.show();
		}

		function get_selected_attributes() {
			let selected_attributes = {};
			me.multiple_variant_dialog.$wrapper.find(".form-column").each((i, col) => {
				if (i === 0) return;
				let attribute_name = $(col).find(".column-label").html().trim();
				selected_attributes[attribute_name] = [];
				let checked_opts = $(col).find(".checkbox input");
				checked_opts.each((i, opt) => {
					if ($(opt).is(":checked")) {
						selected_attributes[attribute_name].push($(opt).attr("data-fieldname"));
					}
				});
			});

			return selected_attributes;
		}

		frm.doc.attributes.forEach(function (d) {
			if (!d.disabled) {
				let p = new Promise((resolve) => {
					if (!d.numeric_values) {
						frappe
							.call({
								method: "frappe.client.get_list",
								args: {
									doctype: "Item Attribute Value",
									filters: [["parent", "=", d.attribute]],
									fields: ["attribute_value"],
									limit_page_length: 0,
									parent: "Item Attribute",
									order_by: "idx",
								},
							})
							.then((r) => {
								if (r.message) {
									attr_val_fields[d.attribute] = r.message.map(function (d) {
										return d.attribute_value;
									});
									resolve();
								}
							});
					} else {
						let values = [];
						for (var i = d.from_range; i <= d.to_range; i = flt(i + d.increment, 6)) {
							values.push(i);
						}
						attr_val_fields[d.attribute] = values;
						resolve();
					}
				});

				promises.push(p);
			}
		}, this);

		Promise.all(promises).then(() => {
			let fields = make_fields_from_attribute_values(attr_val_fields);
			make_and_show_dialog(fields);
		});
	},

	show_single_variant_dialog: function (frm) {
		var fields = [];

		for (var i = 0; i < frm.doc.attributes.length; i++) {
			var fieldtype, desc;
			var row = frm.doc.attributes[i];

			if (!row.disabled) {
				if (row.numeric_values) {
					fieldtype = "Float";
					desc =
						"Min Value: " +
						row.from_range +
						" , Max Value: " +
						row.to_range +
						", in Increments of: " +
						row.increment;
				} else {
					fieldtype = "Data";
					desc = "";
				}
				fields = fields.concat({
					label: row.attribute,
					fieldname: row.attribute,
					fieldtype: fieldtype,
					reqd: 0,
					description: desc,
				});
			}
		}

		if (frm.doc.image) {
			fields.push({
				fieldtype: "Check",
				label: __("Create a variant with the template image."),
				fieldname: "use_template_image",
				default: 0,
			});
		}

		var d = new frappe.ui.Dialog({
			title: __("Create Omni Item Variant"),
			fields: fields,
		});

		d.set_primary_action(__("Create"), function () {
			var args = d.get_values();
			if (!args) return;
			frappe.call({
				method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.get_variant",
				btn: d.get_primary_btn(),
				args: {
					template: frm.doc.name,
					args: d.get_values(),
				},
				callback: function (r) {
					// returns variant item
					if (r.message) {
						var variant = r.message;
						frappe.msgprint_dialog = frappe.msgprint(
							__("Item Variant {0} already exists with same attributes", [
								repl(
									'<a href="/app/item/%(item_encoded)s" class="strong variant-click">%(item)s</a>',
									{
										item_encoded: encodeURIComponent(variant),
										item: variant,
									}
								),
							])
						);
						frappe.msgprint_dialog.hide_on_page_refresh = true;
						frappe.msgprint_dialog.$wrapper
							.find(".variant-click")
							.on("click", function () {
								d.hide();
							});
					} else {
						d.hide();
						frappe.call({
							method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.create_variant",
							args: {
								item: frm.doc.name,
								args: d.get_values(),
								use_template_image: args.use_template_image,
							},
							callback: function (r) {
								var doclist = frappe.model.sync(r.message);
								frappe.set_route("Form", doclist[0].doctype, doclist[0].name);
							},
						});
					}
				},
			});
		});

		d.show();

		$.each(d.fields_dict, function (i, field) {
			if (field.df.fieldtype !== "Data") {
				return;
			}

			$(field.input_area).addClass("ui-front");

			var input = field.$input.get(0);
			input.awesomplete = new Awesomplete(input, {
				minChars: 0,
				maxItems: 99,
				autoFirst: true,
				list: [],
			});
			input.field = field;

			field.$input
				.on("input", function (e) {
					var term = e.target.value;
					frappe.call({
						method: "inno_erp.inno_omnichannel.doctype.omni_item.omni_item.get_omni_item_attribute",
						args: {
							parent: i,
							attribute_value: term,
						},
						callback: function (r) {
							if (r.message) {
								e.target.awesomplete.list = r.message.map(function (d) {
									return d.attribute_value;
								});
							}
						},
					});
				})
				.on("focus", function (e) {
					$(e.target).val("").trigger("input");
				})
				.on("awesomplete-open", () => {
					let modal = field.$input.parents(".modal-dialog")[0];
					if (modal) {
						$(modal).removeClass("modal-dialog-scrollable");
					}
				});
		});
	},
	toggle_attributes(frm) {
		if (
			(frm.doc.has_variants || frm.doc.variant_of) &&
			frm.doc.variant_based_on === "Item Attribute"
		) {
			frm.toggle_display("attributes", true);

			var grid = frm.fields_dict.attributes.grid;

			if (frm.doc.variant_of) {
				// variant

				// value column is displayed but not editable
				grid.set_column_disp("attribute_value", true);
				grid.toggle_enable("attribute_value", false);

				grid.toggle_enable("attribute", false);

				// can't change attributes since they are
				// saved when the variant was created
				frm.toggle_enable("attributes", false);
			} else {
				// template - values not required!

				// make the grid editable
				frm.toggle_enable("attributes", true);

				// value column is hidden
				grid.set_column_disp("attribute_value", false);

				// enable the grid so you can add more attributes
				grid.toggle_enable("attribute", true);
			}
		} else {
			// nothing to do with attributes, hide it
			frm.toggle_display("attributes", false);
		}
		frm.layout.refresh_sections();
	},
	OmniCategorySelect: class {
		constructor(wrapper, frm, disable) {
			this.wrapper = wrapper;
			this.frm = frm;
			this.disable = disable;

			this.category_select = frappe.ui.form.make_control({
				parent: this.wrapper,
				df: {
					fieldname: "category_select",
					fieldtype: "Cascader",
					options: [
						{
							label: "Parent 2",
							value: "parent2",
							children: [
								{ label: "Child 2.1", value: "child2.1" },
								{ label: "Child 2.2", value: "child2.2" },
							],
						},
						{
							label: "Parent 3",
							value: "parent3",
							children: [
								{ label: "Child 3.1", value: "child3.1" },
								{
									label: "Child 3.2",
									value: "child3.2",
									children: [
										{ label: "Grandchild 3.2.1", value: "grandchild3.2.1" },
										{
											label: "Child 3.2.2",
											value: "child3.2.2",
											children: [
												{
													label: "Grandchild 3.2.2.1",
													value: "grandchild3.2.2.1",
												},
												{
													label: "Child 3.2.2.2",
													value: "child3.2.2.2",
													children: [
														{
															label: "Grandchild 3.2.2.2.1",
															value: "grandchild3.2.2.2.1",
														},
														{
															label: "Grandchild 3.2.2.2.2",
															value: "grandchild3.2.2.2.2",
														},
													],
												},
											],
										},
									],
								},
							],
						},
					],
					onchange: () => {
						this.frm.set_value(
							"category",
							this.category_select.get_value()[
								this.category_select.get_value().length - 1
							]
						);
					},
				},
				render_input: true,
			});
			this.set_panel_path(this.frm.doc.category);
		}

		destroy() {
			this.wrapper = null;
			this.category_select = null;
		}

		set_panel_path(value) {
			if (!value || !this.category_select.df.options) {
				return;
			}

			const findPath = (options, value, path = []) => {
				for (const option of options) {
					const newPath = [
						...path,
						{ label: option.label, value: option.value, children: option.children },
					];
					if (option.value === value) {
						return newPath;
					}
					if (option.children) {
						const childPath = findPath(option.children, value, newPath);
						if (childPath) {
							return childPath;
						}
					}
				}
				return null;
			};

			const cascaderPath = findPath(this.category_select.df.options, value);
			if (cascaderPath) {
				const values = cascaderPath.map((item) => item.value);
				this.category_select.cascaderPath = cascaderPath;
				this.category_select.set_value(values);
				this.category_select.update_label();
			}
		}
	},
});
