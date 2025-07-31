import frappe
from erpnext.accounts.doctype.pricing_rule import utils
from erpnext.accounts.doctype.pricing_rule.utils import (
    _get_pricing_rules,
    filter_pricing_rule_based_on_condition,
    filter_pricing_rules,
    get_applied_pricing_rules,
)
from erpnext.accounts.doctype.pricing_rule.utils import (
    apply_pricing_rule_on_transaction as erpnext_apply_pricing_rule_on_transaction,
)
from frappe import _, bold
from frappe.utils import cint, fmt_money


def inno_get_pricing_rules(args, doc=None):
    selected_rules = []

    if args.get("_pricing_rules"):
        selected_rules = get_applied_pricing_rules(args.get("_pricing_rules"))

    pricing_rules = []
    values = {}

    if not frappe.db.exists("Pricing Rule", {"disable": 0, args.transaction_type: 1}):
        return

    for apply_on in ["Item Code", "Item Group", "Brand"]:
        pricing_rules.extend(_get_pricing_rules(apply_on, args, values))

    pricing_rules = filter_pricing_rule_based_on_condition(pricing_rules, doc)

    if not pricing_rules:
        return []

    rules = []

    for pricing_rule in pricing_rules:
        rule = filter_pricing_rules(args, pricing_rule, doc)
        if rule:
            rules.append(rule)
    non_coupon_rules = [r for r in rules if r.get("coupon_code_based") == 0]
    coupon_rules = [r for r in rules if r.get("coupon_code_based") == 1]

    filtered_non_coupon = [r for r in non_coupon_rules if r.name in selected_rules]
    filtered_coupon = [r for r in coupon_rules if r.name in selected_rules]
    if len(non_coupon_rules) == 1:
        if len(selected_rules) == 0:
            frappe.msgprint("Pricing rule applied successfully")
            return non_coupon_rules
        filtered_non_coupon = non_coupon_rules

    rule = filtered_non_coupon + filtered_coupon
    return rule


utils.get_pricing_rules = inno_get_pricing_rules


def inno_validate_quantity_and_amount_for_suggestion(
    args, qty, amount, item_code, transaction_type
):
    fieldname, msg = "", ""
    type_of_transaction = "purchase" if transaction_type == "buying" else "sale"

    for field, value in {"min_qty": qty, "min_amt": amount}.items():
        if (
            args.get(field)
            and value < args.get(field)
            and (
                args.get(field)
                - cint(args.get(field) * args.threshold_percentage * 0.01)
            )
            <= value
        ):
            fieldname = field

    for field, value in {"max_qty": qty, "max_amt": amount}.items():
        if (
            args.get(field)
            and value > args.get(field)
            and (
                args.get(field)
                + cint(args.get(field) * args.threshold_percentage * 0.01)
            )
            >= value
        ):
            fieldname = field

    if fieldname:
        msg = _(
            "If you {0} {1} quantities of the item {2}, the scheme {3} will be applied on the item."
        ).format(
            type_of_transaction, args.get(fieldname), bold(item_code), bold(args.title)
        )

        if fieldname in ["min_amt", "max_amt"]:
            msg = _(
                "If you {0} {1} worth item {2}, the scheme {3} will be applied on the item."
            ).format(
                type_of_transaction,
                fmt_money(args.get(fieldname), currency=args.get("currency")),
                bold(item_code),
                bold(args.title),
            )

    return msg


utils.validate_quantity_and_amount_for_suggestion = (
    inno_validate_quantity_and_amount_for_suggestion
)


def inno_apply_pricing_rule_on_transaction(doc):
    if (
        doc.doctype
        in ["Material Request", "Sales Invoice", "Sales Order", "POS Invoice"]
        or doc.ignore_pricing_rule
    ):
        return

    erpnext_apply_pricing_rule_on_transaction(doc)


utils.apply_pricing_rule_on_transaction = inno_apply_pricing_rule_on_transaction
