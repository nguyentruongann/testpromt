const PRICING_RULE_TABLE_FIELDS = [
    {
        fieldtype: "Data",
        fieldname: "pricing_rule",
        label: __("Rule Code"),
        in_list_view: true,
        read_only: 1,
        columns: 2,
    },
    {
        fieldtype: "Data",
        fieldname: "title",
        label: __("Title"),
        in_list_view: true,
        read_only: 1,
        columns: 2,
    },
    {
        fieldtype: "Data",
        fieldname: "type",
        label: __("Type"),
        in_list_view: true,
        read_only: 1,
        columns: 1,
    },
    {
        fieldtype: "Data",
        fieldname: "detail",
        label: __("Free/Discount"),
        in_list_view: true,
        read_only: 1,
        columns: 4,
    },
    {
        fieldtype: "Check",
        fieldname: "selected",
        label: __("Selected"),
        in_list_view: true,
        columns: 1,
    },
];

const SUGGEST_RULE_FIELDS = [
    {
        fieldtype: "Data",
        fieldname: "title",
        label: __("Title"),
        in_list_view: true,
        read_only: 2,
    },
    {
        fieldtype: "Data",
        fieldname: "name",
        label: __("Rule Code"),
        in_list_view: true,
        read_only: 1,
    },
    {
        fieldtype: "Data",
        fieldname: "suggestion_message",
        label: __("Message"),
        in_list_view: true,
        read_only: 7,
    },
];

erpnext.TransactionController = class InnoTransactionController extends (
    erpnext.TransactionController
) {
    get_coupon_code(doc) {
        return doc.doctype === "Sales Invoice" ? doc.custom_coupon_code : doc.coupon_code;
    }

    onload() {
        super.onload();
        if (["Sales Invoice", "Sales Order", "POS Invoice"].includes(this.frm.doc.doctype)) {
            this.frm.__selected_pricing_rules = {};
            this.frm.__is_applying_pricing_from_dialog = false;
            this.frm.__selected_pricing_rules.transaction = {
                pricing_rule: null,
                coupon_pricing_rule: null,
            };
        }
    }

    filter_not_free_or_empty_item(items) {
        return items.filter((item) => item?.item_code && !item.is_free_item);
    }

    validate_pricing_rule_items() {
        const me = this;
        return this.filter_not_free_or_empty_item(me.frm.doc.items).map((item) => ({
            doctype: item.doctype,
            name: item.name,
            item_code: item.item_code,
            item_group: item.item_group,
            brand: item.brand,
            qty: item.qty || 0,
            stock_qty: item.stock_qty || 0,
            price_list_rate: item.price_list_rate || 0,
            uom: item.uom,
            stock_uom: item.stock_uom,
            parent: me.frm.doc.name,
            parenttype: me.frm.doc.doctype,
            child_docname: item.name,
            conversion_factor: item.conversion_factor || 1.0,
            discount_percentage: item.discount_percentage || 0,
            discount_amount: item.discount_amount || 0,
            pricing_rules: item.pricing_rules || "",
        }));
    }

    handle_dialog_fields(item_details) {
        const me = this;
        let fields = [];
        const items = this.filter_not_free_or_empty_item(me.frm.doc.items);
        let idx = 1;
        for (const item of items) {
            const item_result = item_details.find((res) => res.item_code === item.item_code) || {};
            const pricing_rules = item_result.pricing_rules_list || [];
            const suggestion_rules = item_result.suggestion_rules || [];
            fields.push({
                fieldtype: "Section Break",
                label: __("Item {0}: {1} - {2}", [idx++, item.item_code, item.item_name]),
            });
            fields.push({
                fieldtype: "Table",
                fieldname: `pricing_table_${frappe.scrub(item.item_code)}`,
                label: __("Pricing Rules"),
                cannot_add_rows: true,
                in_place_edit: true,
                cannot_delete_rows: true,
                data: [...pricing_rules].map((rule) => {
                    let is_selected = false;
                    if (
                        me.frm.__selected_pricing_rules &&
                        me.frm.__selected_pricing_rules[item.item_code]
                    ) {
                        is_selected =
                            me.frm.__selected_pricing_rules[item.item_code].pricing_rule ===
                            rule.pricing_rule;
                    }
                    return {
                        pricing_rule: rule.pricing_rule,
                        title: rule.details.title,
                        type: rule.details.price_or_product_discount,
                        detail: (() => {
                            const type = rule.details.price_or_product_discount;
                            if (type === "Product" && rule.details.free_item) {
                                return __("Free: {0} (Quantity: {1})", [
                                    rule.details.free_item,
                                    rule.details.free_qty
                                ]);
                            } else if (type === "Price") {
                                if (rule.details.discount_percentage > 0)
                                    return __("Discount: {0}%", [rule.details.discount_percentage]);
                                if (rule.details.discount_amount > 0)
                                    return __("Discount: {0}", [
                                        fmt_money(rule.details.discount_amount, me.frm.doc.currency)
                                    ]);
                                if (rule.details.rate > 0)
                                    return __("Price: {0}", [
                                        fmt_money(rule.details.rate, me.frm.doc.currency)
                                    ]);
                            }
                            return "";
                        })(),
                        selected: is_selected ? 1 : 0,
                        is_coupon_rule: rule.details.coupon_code_based ? 1 : 0,
                    };
                }),
                fields: PRICING_RULE_TABLE_FIELDS,
            });
            if (suggestion_rules.length > 0) {
                fields.push({
                    fieldtype: "Table",
                    fieldname: `suggestion_table_${frappe.scrub(item.item_code)}`,
                    label: __("Suggested Rules"),
                    cannot_add_rows: true,
                    in_place_edit: true,
                    read_only: 1,
                    cannot_delete_rows: true,
                    data: suggestion_rules.map((rule) => ({
                        title: rule.title,
                        name: rule.name,
                        suggestion_message: rule.suggestion_message,
                    })),
                    fields: SUGGEST_RULE_FIELDS,
                });
            }
        }
        return fields;
    }

    handle_transaction_dialog_fields(transaction_details) {
        const me = this;
        let fields = [];
        const pricing_rules = transaction_details.pricing_rules_list || [];
        const suggestion_rules = transaction_details.suggestion_rules || [];
        fields.push({
            fieldtype: "Section Break",
            label: __("Transaction Pricing Rules"),
        });
        fields.push({
            fieldtype: "Table",
            fieldname: "pricing_table_transaction",
            label: __("Pricing Rules"),
            cannot_add_rows: true,
            in_place_edit: true,
            cannot_delete_rows: true,
            data: pricing_rules.map((rule) => {
                let is_selected = false;
                if (
                    me.frm.__selected_pricing_rules &&
                    me.frm.__selected_pricing_rules.transaction
                ) {
                    is_selected =
                        me.frm.__selected_pricing_rules.transaction.pricing_rule ===
                            rule.details.name ||
                        me.frm.__selected_pricing_rules.transaction.coupon_pricing_rule ===
                            rule.details.name;
                }
                return {
                    pricing_rule: rule.details.name,
                    title: rule.title,
                    type: rule.details.price_or_product_discount,
                    detail: (() => {
                        const type = rule.details.price_or_product_discount;
                        if (type === "Product" && rule.details.free_item) {
                            return __("Free: {0} (Quantity: {1})", [
                                rule.details.free_item,
                                rule.details.free_qty
                            ]);
                        } else if (type === "Price") {
                            if (rule.details.discount_percentage > 0)
                                return __("Discount: {0}%", [rule.details.discount_percentage]);
                            if (rule.details.discount_amount > 0)
                                return __("Discount: {0}", [
                                    fmt_money(rule.details.discount_amount, me.frm.doc.currency)
                                ]);
                            if (rule.details.rate > 0)
                                return __("Price: {0}", [
                                    fmt_money(rule.details.rate, me.frm.doc.currency)
                                ]);
                        }
                        return "";
                    })(),
                    selected: is_selected ? 1 : 0,
                    is_coupon_rule: rule.details.coupon_code_based ? 1 : 0,
                };
            }),
            fields: PRICING_RULE_TABLE_FIELDS,
        });
        if (suggestion_rules.length > 0) {
            fields.push({
                fieldtype: "Table",
                fieldname: "suggestion_table_transaction",
                label: __("Suggested Rules"),
                cannot_add_rows: true,
                in_place_edit: true,
                read_only: 1,
                cannot_delete_rows: true,
                data: suggestion_rules.map((rule) => ({
                    title: rule.title,
                    name: rule.name,
                    suggestion_message: rule.suggestion_message,
                })),
                fields: SUGGEST_RULE_FIELDS,
            });
        }
        return fields;
    }

    show_pricing_rule_dialog() {
        const me = this;
        const items = this.validate_pricing_rule_items();
        if (!items.length) {
            frappe.msgprint(__("No valid items to apply pricing rules."));
            return;
        }

        frappe.call({
            method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.get_all_pricing_rules_for_item",
            args: {
                args: {
                    items: items,
                    customer: me.frm.doc.customer || me.frm.doc.party_name,
                    transaction_date: me.frm.doc.transaction_date || me.frm.doc.posting_date,
                    company: me.frm.doc.company,
                    transaction_type: "selling",
                    price_list: me.frm.doc.selling_price_list,
                    currency: me.frm.doc.currency,
                    conversion_rate: me.frm.doc.conversion_rate,
                    plc_conversion_rate: me.frm.doc.plc_conversion_rate,
                    ignore_pricing_rule: 0,
                    coupon_code: me.get_coupon_code(me.frm.doc),
                },
            },
            freeze: true,
            freeze_message: __("Fetching pricing rules..."),
            callback: function (r_item) {
                if (r_item.exc || !r_item.message) {
                    frappe.msgprint(__("No pricing rules found or an error occurred."));
                    return;
                }
                frappe.call({
                    method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.get_all_pricing_rules_for_transaction",
                    args: {
                        args: {
                            transaction_type: "selling",
                            transaction_date:
                                me.frm.doc.transaction_date || me.frm.doc.posting_date,
                            company: me.frm.doc.company,
                            customer: me.frm.doc.customer || me.frm.doc.party_name,
                            doctype: me.doctype || "Sales Order",
                            total_qty: me.frm.doc.total_qty,
                            total: me.frm.doc.total,
                            coupon_code: me.get_coupon_code(me.frm.doc),
                        },
                    },
                    callback: function (r_transaction) {
                        if (r_transaction.exc || !r_transaction.message) {
                            frappe.msgprint(__("No transaction pricing rules found."));
                        }
                        let item_fields = me.handle_dialog_fields(r_item.message);
                        let transaction_fields = me.handle_transaction_dialog_fields(
                            r_transaction.message || {
                                pricing_rules_list: [],
                                suggestion_rules: [],
                            }
                        );
                        let all_fields = item_fields.concat(transaction_fields);

                        const dialog = new frappe.ui.Dialog({
                            title: __("Select Pricing Rules"),
                            size: "extra-large",
                            fields: all_fields,
                            primary_action_label: __("Done"),
                            primary_action: () => {
                                dialog.hide();
                            },
                        });
                        dialog.show();

                        const dialog_items = me.filter_not_free_or_empty_item(me.frm.doc.items);
                        for (const item of dialog_items) {
                            const scrub_item_code = frappe.scrub(item.item_code);
                            if (dialog.fields_dict[`suggestion_table_${scrub_item_code}`]) {
                                dialog.fields_dict[
                                    `suggestion_table_${scrub_item_code}`
                                ].grid.wrapper
                                    .find(".row-check")
                                    .hide();
                            }
                            if (dialog.fields_dict[`pricing_table_${scrub_item_code}`]) {
                                dialog.fields_dict[`pricing_table_${scrub_item_code}`].grid.wrapper
                                    .find(".row-check")
                                    .on("click", function (e) {
                                        let row = $(this).closest(".grid-row");
                                        let row_idx = row.data("idx");
                                        let table_data = dialog.get_value(
                                            `pricing_table_${scrub_item_code}`
                                        );
                                        let selected_row = table_data[row_idx - 1];
                                        table_data.forEach((row) => {
                                            row.selected =
                                                row.pricing_rule === selected_row.pricing_rule
                                                    ? row.selected
                                                        ? 0
                                                        : 1
                                                    : 0;
                                        });
                                        dialog.set_value(
                                            `pricing_table_${scrub_item_code}`,
                                            table_data
                                        );

                                        const selected_rule =
                                            table_data.find((row) => row.selected)?.pricing_rule ||
                                            null;

                                        me.frm.__selected_pricing_rules[item.item_code] = me.frm
                                            .__selected_pricing_rules[item.item_code] || {
                                            pricing_rule: null,
                                            coupon_pricing_rule: null,
                                        };
                                        me.frm.__selected_pricing_rules[
                                            item.item_code
                                        ].pricing_rule = selected_rule;

                                        const pricing_rules_array = selected_rule
                                            ? [selected_rule]
                                            : [];
                                        frappe.model.set_value(
                                            item.doctype,
                                            item.name,
                                            "pricing_rules",
                                            pricing_rules_array.length > 0
                                                ? JSON.stringify(pricing_rules_array)
                                                : ""
                                        );

                                        frappe.run_serially([
                                            () => dialog.hide(),
                                            () => me.apply_pricing_rule_from_dialog(),
                                            () => me.show_pricing_rule_dialog(),
                                        ]);
                                    });
                            }
                        }
                        if (dialog.fields_dict["suggestion_table_transaction"]) {
                            dialog.fields_dict["suggestion_table_transaction"].grid.wrapper
                                .find(".row-check")
                                .hide();
                        }
                        if (dialog.fields_dict["pricing_table_transaction"]) {
                            dialog.fields_dict["pricing_table_transaction"].grid.wrapper
                                .find(".row-check")
                                .on("click", function (e) {
                                    let row = $(this).closest(".grid-row");
                                    let row_idx = row.data("idx");
                                    let table_data = dialog.get_value("pricing_table_transaction");
                                    let selected_row = table_data[row_idx - 1];
                                    table_data.forEach((row) => {
                                        row.selected =
                                            row.pricing_rule === selected_row.pricing_rule
                                                ? row.selected
                                                    ? 0
                                                    : 1
                                                : 0;
                                    });
                                    dialog.set_value("pricing_table_transaction", table_data);

                                    const selected_transaction_rule =
                                        table_data.find((row) => row.selected)?.pricing_rule ||
                                        null;

                                    me.frm.__selected_pricing_rules.transaction = me.frm
                                        .__selected_pricing_rules.transaction || {
                                        pricing_rule: null,
                                        coupon_pricing_rule: null,
                                    };

                                    me.frm.__selected_pricing_rules.transaction.pricing_rule =
                                        selected_transaction_rule;

                                    frappe.run_serially([
                                        () => dialog.hide(),
                                        () => me.apply_pricing_rule_from_dialog(),
                                        () => me.show_pricing_rule_dialog(),
                                    ]);
                                });
                        }
                    },
                    error: function () {
                        frappe.msgprint(
                            __("An error occurred while fetching transaction pricing rules.")
                        );
                    },
                });
            },
            error: function () {
                frappe.msgprint(
                    __("An error occurred while fetching pricing rules. Please try again.")
                );
            },
        });
    }

    apply_pricing_rule_from_dialog() {
        let me = this;
        let items = me.filter_not_free_or_empty_item(me.frm.doc.items);

        me.frm.__is_applying_pricing_from_dialog = true;

        return new Promise((resolve) => {
            frappe.run_serially([
                () => {
                    const validate_items = this.validate_pricing_rule_items();
                    return frappe.call({
                        method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.get_all_pricing_rules_for_item",
                        args: {
                            args: {
                                items: validate_items,
                                customer: me.frm.doc.customer || me.frm.doc.party_name,
                                transaction_date:
                                    me.frm.doc.transaction_date || me.frm.doc.posting_date,
                                company: me.frm.doc.company,
                                transaction_type: "selling",
                                price_list: me.frm.doc.selling_price_list,
                                currency: me.frm.doc.currency,
                                conversion_rate: me.frm.doc.conversion_rate,
                                plc_conversion_rate: me.frm.doc.plc_conversion_rate,
                                ignore_pricing_rule: 0,
                                coupon_code: me.get_coupon_code(me.frm.doc),
                            },
                        },
                        callback: function (r_item) {
                            if (!r_item.exc && r_item.message) {
                                for (const item of me.frm.doc.items) {
                                    if (
                                        me.frm.__selected_pricing_rules &&
                                        me.frm.__selected_pricing_rules[item.item_code]
                                    ) {
                                        const item_result =
                                            r_item.message.find(
                                                (res) => res.item_code === item.item_code
                                            ) || {};
                                        const pricing_rules = item_result.pricing_rules_list || [];
                                        const coupon_rules =
                                            item_result.coupon_pricing_rules || [];
                                        const current_rule =
                                            me.frm.__selected_pricing_rules[item.item_code]
                                                .pricing_rule;
                                        const current_coupon =
                                            me.frm.__selected_pricing_rules[item.item_code]
                                                .coupon_pricing_rule;

                                        const selected_rule =
                                            pricing_rules.find(
                                                (rule) => rule.pricing_rule === current_rule
                                            ) ||
                                            coupon_rules.find(
                                                (rule) => rule.pricing_rule === current_coupon
                                            );
                                        if (
                                            selected_rule &&
                                            selected_rule.details.price_or_product_discount ===
                                                "Product"
                                        ) {
                                            frappe.model.set_value(
                                                item.doctype,
                                                item.name,
                                                "discount_percentage",
                                                0
                                            );
                                            frappe.model.set_value(
                                                item.doctype,
                                                item.name,
                                                "discount_amount",
                                                0
                                            );
                                            frappe.model.set_value(
                                                item.doctype,
                                                item.name,
                                                "rate",
                                                item.price_list_rate || 0
                                            );
                                        } else if (selected_rule) {
                                            const rule_type = selected_rule.rate_or_discount;
                                            if (rule_type === "Rate") {
                                                frappe.model.set_value(
                                                    item.doctype,
                                                    item.name,
                                                    "discount_percentage",
                                                    0
                                                );
                                                frappe.model.set_value(
                                                    item.doctype,
                                                    item.name,
                                                    "discount_amount",
                                                    0
                                                );
                                            } else if (
                                                rule_type === "Discount Percentage" ||
                                                rule_type === "Discount Amount"
                                            ) {
                                                frappe.model.set_value(
                                                    item.doctype,
                                                    item.name,
                                                    "rate",
                                                    item.price_list_rate || 0
                                                );
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    });
                },
                () => {
                    let non_free_items = [];
                    for (const item of me.frm.doc.items) {
                        me.remove_pricing_rule(item);
                        if (!item.is_free_item) {
                            non_free_items.push(item);
                        }
                    }
                    me.frm.doc.items = non_free_items;
                    me.frm.refresh_field("items");
                },
                () => {
                    for (const item of items) {
                        if (!item) continue;
                        if (!me.is_a_mapped_document(item)) {
                            frappe.run_serially([
                                () => me.remove_pricing_rule_for_item(item),
                                () => me.in_apply_price_list = false,
                                () => me.apply_price_list(item, true),
                                () => me.apply_pricing_rule(item, true),
                            ]);
                        } else {
                            me.conversion_factor(me.frm.doc, item.doctype, item.name, true);
                        }
                    }
                },
                () => {
                    if (
                        me.frm.__selected_pricing_rules &&
                        me.frm.__selected_pricing_rules.transaction
                    ) {
                        const transaction_selected = me.frm.__selected_pricing_rules.transaction;
                        const doc_copy = Object.assign({}, me.frm.doc);
                        if (doc_copy.doctype === "Sales Invoice") {
                            doc_copy.coupon_code = doc_copy.custom_coupon_code;
                        }
                        return frappe.call({
                            method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.inno_apply_transaction_pricing_rule",
                            args: {
                                pricing_rule: transaction_selected.pricing_rule,
                                doc: doc_copy,
                            },
                            callback: function (r) {
                                if (!r.exc && r.message) {
                                    me.frm.set_value(
                                        "additional_discount_percentage",
                                        r.message.additional_discount_percentage
                                    );
                                    me.frm.set_value(
                                        "discount_amount",
                                        r.message.discount_amount
                                    );
                                    if (
                                        r.message.free_item_data &&
                                        r.message.free_item_data.length > 0
                                    ) {
                                        const args = {
                                            free_item_data: r.message.free_item_data.map(
                                                (free_item) => {
                                                    free_item.delivery_date =
                                                        me.frm.doc.items[0]
                                                            ?.delivery_date ||
                                                        me.frm.doc.delivery_date ||
                                                        "";
                                                    return free_item;
                                                }
                                            ),
                                        };
                                        me.apply_product_discount(args);
                                    }
                                    if (
                                        frappe.meta.has_field(
                                            me.frm.doc.doctype,
                                            "transaction_pricing_rules"
                                        )
                                    ) {
                                        me.frm.set_value(
                                            "transaction_pricing_rules",
                                            r.message.applied_pricing_rules
                                        );
                                    }
                                }
                            },
                        });
                    }
                },
                () => {
                    me.calculate_taxes_and_totals();
                    me.frm.__is_applying_pricing_from_dialog = false;
                    resolve();
                },
            ]);
        });
    }

    qty(doc, cdt, cdn) {
        if (!["Sales Invoice", "Sales Order", "POS Invoice"].includes(this.frm.doc.doctype) || this.frm.__is_applying_pricing_from_dialog) {
            return super.qty(doc, cdt, cdn);
        }

        const me = this;
        const items = this.validate_pricing_rule_items();

        cur_frm.set_value(this.frm.doc.doctype === "Sales Invoice" ? "custom_coupon_code" : "coupon_code", "");

        const updateItemSelectedRules = (item, itemResult) => {
            if (!me.frm.__selected_pricing_rules?.[item.item_code]) return;

            const pricingRules = itemResult?.pricing_rules_list || [];
            const couponRules = itemResult?.coupon_pricing_rules || [];
            const selected = me.frm.__selected_pricing_rules[item.item_code];

            if (selected.pricing_rule && !pricingRules.some(rule => rule.pricing_rule === selected.pricing_rule)) {
                selected.pricing_rule = null;
            }
            if (selected.coupon_pricing_rule && !couponRules.some(rule => rule.pricing_rule === selected.coupon_pricing_rule)) {
                selected.coupon_pricing_rule = null;
            }

            const pricingRulesArray = [
                ...(selected.pricing_rule ? [selected.pricing_rule] : []),
                ...(selected.coupon_pricing_rule ? [selected.coupon_pricing_rule] : [])
            ];
            frappe.model.set_value(item.doctype, item.name, "pricing_rules",
                pricingRulesArray.length ? JSON.stringify(pricingRulesArray) : "");
        };

        const updateTransactionSelectedRule = (r_transaction) => {
            if (!r_transaction.exc && r_transaction.message?.pricing_rules_list) {
                const pricingRules = r_transaction.message.pricing_rules_list;
                if (me.frm.__selected_pricing_rules?.transaction) {
                    const selected = me.frm.__selected_pricing_rules.transaction;
                    if (selected.pricing_rule && !pricingRules.some(rule => rule.details.name === selected.pricing_rule)) {
                        selected.pricing_rule = null;
                    }
                    if (selected.coupon_pricing_rule && !pricingRules.some(rule => rule.details.name === selected.coupon_pricing_rule)) {
                        selected.coupon_pricing_rule = null;
                    }
                }
            }
        };

        return frappe.run_serially([
            () => frappe.call({
                method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.get_all_pricing_rules_for_item",
                args: {
                    args: {
                        items,
                        customer: me.frm.doc.customer || me.frm.doc.party_name,
                        transaction_date: me.frm.doc.transaction_date || me.frm.doc.posting_date,
                        company: me.frm.doc.company,
                        transaction_type: "selling",
                        price_list: me.frm.doc.selling_price_list,
                        currency: me.frm.doc.currency,
                        conversion_rate: me.frm.doc.conversion_rate,
                        plc_conversion_rate: me.frm.doc.plc_conversion_rate,
                        ignore_pricing_rule: 0,
                        coupon_code: me.get_coupon_code(me.frm.doc)
                    }
                },
                callback: (r_item) => {
                    if (!r_item.exc && r_item.message) {
                        me.frm.doc.items.forEach(item => {
                            const itemResult = r_item.message.find(res => res.item_code === item.item_code) || {};
                            updateItemSelectedRules(item, itemResult);
                        });
                    }
                }
            }),
            () => frappe.call({
                method: "inno_erp.inno_account.overrides.pricing_rule.pricing_rule.get_all_pricing_rules_for_transaction",
                args: {
                    args: {
                        transaction_type: "selling",
                        transaction_date: me.frm.doc.transaction_date || me.frm.doc.posting_date,
                        company: me.frm.doc.company,
                        customer: me.frm.doc.customer || me.frm.doc.party_name,
                        doctype: me.doctype || "Sales Order",
                        total_qty: me.frm.doc.total_qty,
                        total: me.frm.doc.total,
                        coupon_code: me.get_coupon_code(me.frm.doc)
                    }
                },
                callback: (r_transaction) => {
                    updateTransactionSelectedRule(r_transaction);
                    return me.apply_pricing_rule_from_dialog();
                }
            })
        ]);
    }
	_get_args(item) {
		var me = this;
		return {
			"items": this._get_item_list(item),
			"customer": me.frm.doc.customer || me.frm.doc.party_name,
			"quotation_to": me.frm.doc.quotation_to,
			"customer_group": me.frm.doc.customer_group,
			"territory": me.frm.doc.territory,
			"supplier": me.frm.doc.supplier,
			"supplier_group": me.frm.doc.supplier_group,
			"currency": me.frm.doc.currency,
			"conversion_rate": me.frm.doc.conversion_rate,
			"price_list": me.frm.doc.selling_price_list || me.frm.doc.buying_price_list,
			"price_list_currency": me.frm.doc.price_list_currency,
			"plc_conversion_rate": me.frm.doc.plc_conversion_rate,
			"company": me.frm.doc.company,
			"transaction_date": me.frm.doc.transaction_date || me.frm.doc.posting_date,
			"campaign": me.frm.doc.campaign,
			"sales_partner": me.frm.doc.sales_partner,
			"ignore_pricing_rule": me.frm.doc.ignore_pricing_rule,
			"doctype": me.frm.doc.doctype,
			"name": me.frm.doc.name,
			"is_return": cint(me.frm.doc.is_return),
			"update_stock": ['Sales Invoice', 'Purchase Invoice'].includes(me.frm.doc.doctype) ? cint(me.frm.doc.update_stock) : 0,
			"conversion_factor": me.frm.doc.conversion_factor,
			"pos_profile": me.frm.doc.doctype == 'Sales Invoice' ? me.frm.doc.pos_profile : '',
			"coupon_code": me.frm.doc.coupon_code || me.frm.doc.custom_coupon_code,
			"is_internal_supplier": me.frm.doc.is_internal_supplier,
			"is_internal_customer": me.frm.doc.is_internal_customer,
		};
	}


    _get_item_list(item) {
        var me = this;
        var item_list = [];
        var append_item = function (d) {
            if (d.item_code) {
                let selected_rules =
                    me.frm.__selected_pricing_rules && me.frm.__selected_pricing_rules[d.item_code]
                        ? me.frm.__selected_pricing_rules[d.item_code]
                        : { pricing_rule: null, coupon_pricing_rule: null };

                let pricing_rules_array = [];
                if (selected_rules.pricing_rule) {
                    pricing_rules_array.push(selected_rules.pricing_rule);
                }
                if (selected_rules.coupon_pricing_rule) {
                    pricing_rules_array.push(selected_rules.coupon_pricing_rule);
                }

                pricing_rules_array = pricing_rules_array.slice(0, 2);
                item_list.push({
                    doctype: d.doctype,
                    name: d.name,
                    child_docname: d.name,
                    item_code: d.item_code,
                    item_group: d.item_group,
                    brand: d.brand,
                    qty: d.qty,
                    stock_qty: d.stock_qty,
                    uom: d.uom,
                    stock_uom: d.stock_uom,
                    parenttype: d.parenttype,
                    parent: d.parent,
                    pricing_rules: d.pricing_rules,
                    is_free_item: d.is_free_item,
                    warehouse: d.warehouse,
                    serial_no: d.serial_no,
                    batch_no: d.batch_no,
                    price_list_rate: d.price_list_rate,
                    conversion_factor: d.conversion_factor || 1.0,
                    discount_percentage: d.discount_percentage,
                    discount_amount: d.discount_amount,
                    _pricing_rules:
                        pricing_rules_array.length > 0 ? JSON.stringify(pricing_rules_array) : "",
                });

                if (
                    (in_list([
                        "Quotation Item",
                        "Sales Order Item",
                        "Delivery Note Item",
                        "Sales Invoice Item",
                        "Purchase Invoice Item",
                        "Purchase Order Item",
                        "Purchase Receipt Item",
                    ]),
                    d.doctype)
                ) {
                    item_list[0]["margin_type"] = d.margin_type;
                    item_list[0]["margin_rate_or_amount"] = d.margin_rate_or_amount;
                }
            }
        };

        if (item) {
            append_item(item);
        } else {
            $.each(this.frm.doc["items"] || [], function (i, d) {
                append_item(d);
            });
        }
        return item_list;
    }
};

erpnext.TransactionController = erpnext.TransactionController;