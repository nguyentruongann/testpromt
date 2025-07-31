import json

import frappe
import frappe as _
from frappe.desk.form.save import savedocs
from frappe.model.mapper import get_mapped_doc


@frappe.whitelist(methods=["GET"])
def list_applied_free_items(source_name: str):
    doc = frappe.get_doc("POS Invoice", source_name)
    data = doc.as_dict()
    rule_to_purchased = {}
    for pr in data["pricing_rules"]:
        rule = pr["pricing_rule"]
        item_code = pr["item_code"]
        rule_to_purchased[rule] = item_code

    free_items = []
    for item in data["items"]:
        if item["is_free_item"] == 1:
            pricing_rule = item.get("pricing_rules", None)
            if pricing_rule:
                free_code = item["item_code"]
                purchased = None
                if isinstance(pricing_rule, str):
                    pricing_rule = pricing_rule.strip()
                purchased = rule_to_purchased.get(pricing_rule, "Unknown")
                if purchased:
                    free_items.append(
                        {
                            "item_code": purchased,
                            "free_item_code": free_code,
                        }
                    )

    return free_items


@frappe.whitelist(methods=["GET"])
def make_exchange_doc(doctype: str, source_name: str, target_doc=None):
    if doctype not in ["Sales Invoice", "POS Invoice"]:
        frappe.throw(
            _(
                "This function only supports Sales Invoice or POS Invoice as source doctype."
            )
        )

    source_doc = frappe.get_doc(doctype, source_name)
    if not source_doc.is_return:
        frappe.throw(_("Source document must be a return invoice."))

    if doctype == "POS Invoice":
        inv_consolidated_invoice, inv_is_pos = frappe.db.get_value(
            "POS Invoice", source_name, ["consolidated_invoice", "is_pos"]
        )
        if inv_consolidated_invoice and inv_is_pos:
            frappe.throw(
                _("Cannot create exchange for consolidated invoice {0}.").format(
                    source_name
                ),
                title=_("Cannot Create Exchange"),
            )
    elif doctype == "Sales Invoice":
        inv_is_consolidated, inv_is_pos = frappe.db.get_value(
            "Sales Invoice", source_name, ["is_consolidated", "is_pos"]
        )
        if inv_is_consolidated and inv_is_pos:
            frappe.throw(
                _("Cannot create exchange for consolidated invoice {0}.").format(
                    source_name
                ),
                title=_("Cannot Create Exchange"),
            )

    def set_missing_values(source, target):
        target.custom_is_exchange = 1
        target.custom_exchange_against = source.name
        target.is_return = 0
        target.ignore_pricing_rule = 1
        target.pricing_rules = []
        target.is_pos = source.is_pos
        target.update_stock = 1
        target.set_warehouse = source.set_warehouse
        target.selling_price_list = source.selling_price_list

        for exchange_item in source.get("custom_exchange_items") or []:
            new_item = target.append("items", {})
            new_item.update(exchange_item.as_dict())
            if new_item.qty < 0:
                new_item.qty = -new_item.qty
                new_item.stock_qty = -new_item.stock_qty
            new_item.sales_invoice_item = None
            new_item.dn_detail = None
            new_item.so_detail = None
            if new_item.rate == 0:
                update_item_rate(new_item, target)

        for tax in target.get("taxes") or []:
            if tax.tax_amount < 0:
                tax.tax_amount = -tax.tax_amount

        target.run_method("calculate_taxes_and_totals")

    def update_item(source_doc, target_doc, source_parent):
        target_doc.qty = abs(source_doc.qty)
        target_doc.stock_qty = abs(source_doc.stock_qty)
        target_doc.amount = abs(source_doc.amount)
        target_doc.base_amount = abs(source_doc.base_amount)
        target_doc.net_amount = abs(source_doc.net_amount)
        target_doc.base_net_amount = abs(source_doc.base_net_amount)
        target_doc.pricing_rules = None

        if source_doc.is_free_item:
            target_doc.is_free_item = 0
            if target_doc.rate == 0:
                update_item_rate(target_doc, source_parent)

        target_doc.sales_invoice_item = None
        target_doc.dn_detail = None
        target_doc.so_detail = None

    def update_item_rate(item_doc, parent_doc):
        rate = frappe.db.get_value(
            "Item Price",
            {
                "item_code": item_doc.item_code,
                "price_list": parent_doc.selling_price_list,
                "selling": 1,
                "currency": parent_doc.currency,
            },
            "price_list_rate",
        )
        if rate:
            item_doc.rate = rate
            item_doc.base_rate = (
                rate * parent_doc.conversion_rate
                if parent_doc.conversion_rate
                else rate
            )
            item_doc.amount = item_doc.qty * item_doc.rate
            item_doc.base_amount = item_doc.qty * item_doc.base_rate
            item_doc.net_rate = item_doc.rate
            item_doc.net_amount = item_doc.amount
            item_doc.base_net_rate = item_doc.base_rate
            item_doc.base_net_amount = item_doc.base_amount
        else:
            frappe.msgprint(
                _("No selling price found for item {0}. Please set manually.").format(
                    item_doc.item_code
                )
            )

    def item_condition(doc):
        return doc.custom_non_returnable == "Yes" and doc.is_free_item == 1

    doclist = get_mapped_doc(
        doctype,
        source_name,
        {
            doctype: {
                "doctype": doctype,
                "validation": {
                    "docstatus": ["=", 1],
                },
                "field_map": {
                    "posting_date": "posting_date",
                    "customer": "customer",
                    "company": "company",
                    "currency": "currency",
                    "selling_price_list": "selling_price_list",
                },
            },
            doctype + " Item": {
                "doctype": doctype + " Item",
                "field_map": {"serial_no": "serial_no", "batch_no": "batch_no"},
                "postprocess": update_item,
                "condition": item_condition,
            },
        },
        target_doc,
        set_missing_values,
    )

    return doclist


@frappe.whitelist(methods=["POST"])
def savedoc(doc, action):
    return savedocs(json.dumps(doc), action=action)
