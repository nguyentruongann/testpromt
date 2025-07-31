import json

import frappe
from erpnext.accounts.doctype.pricing_rule import pricing_rule
from erpnext.accounts.doctype.pricing_rule.pricing_rule import (
    get_pricing_rule_details,
    set_transaction_type,
    update_args_for_pricing_rule,
    update_pricing_rule_uom,
)
from erpnext.accounts.doctype.pricing_rule.utils import (
    _get_pricing_rules,
    filter_pricing_rule_based_on_condition,
    filter_pricing_rules_for_qty_amount,
    get_applied_pricing_rules,
    get_other_conditions,
    get_pricing_rule_items,
    get_qty_amount_data_for_cumulative,
)
from frappe import _
from frappe.utils import cint, flt, getdate, today

from .utils import inno_validate_quantity_and_amount_for_suggestion


@frappe.whitelist(methods=["POST"])
def get_all_pricing_rules_for_item(args, doc=None):
    args = frappe._dict(json.loads(args) if isinstance(args, str) else args)
    doc = frappe.get_doc(json.loads(doc)) if isinstance(doc, str) else doc

    if not args.get("transaction_type"):
        set_transaction_type(args)

    item_list = args.pop("items", []) or []
    out = []

    for item in item_list:
        args_copy = args.copy().update(item)
        item_details = frappe._dict(
            {
                "pricing_rules_list": [],
                "coupon_pricing_rules": [],
                "suggestion_rules": [],
                "non_applicable_rules": [],
                "item_code": args_copy.get("item_code"),
            }
        )

        # Fix: Bổ sung item_group và brand nếu thiếu
        if not args_copy.get("item_group") or not args_copy.get("brand"):
            if args_copy.get("item_code"):
                try:
                    item_doc = frappe.get_doc("Item", args_copy.get("item_code"))
                    if not args_copy.get("item_group"):
                        args_copy["item_group"] = item_doc.item_group
                    if not args_copy.get("brand"):
                        args_copy["brand"] = item_doc.brand
                except frappe.DoesNotExistError:
                    pass  # Bỏ qua nếu Item không tồn tại

        update_args_for_pricing_rule(args_copy)

        pricing_rules = []
        values = {}  # Sửa từ [] thành {} (values là dict)
        for apply_on in ["Item Code", "Item Group", "Brand"]:
            rules = _get_pricing_rules(apply_on, args_copy, values)
            pricing_rules.extend(rules)

        if not pricing_rules:
            out.append(item_details)
            continue

        rules, coupon_rules, suggestions, non_applicable = [], [], [], []
        qty = flt(args_copy.get("qty"))
        amount = flt(args_copy.get("price_list_rate")) * qty

        for rule in pricing_rules:
            if isinstance(rule, str):
                rule = frappe.get_cached_doc("Pricing Rule", rule)
                update_pricing_rule_uom(rule, args_copy)
                rule.apply_rule_on_other_items = (
                    get_pricing_rule_items(rule, rule.apply_rule_on_other) or []
                )

            coupon_valid = rule.coupon_code_based != 1 or (
                args_copy.get("coupon_code")
                == frappe.db.get_value(
                    "Coupon Code", {"pricing_rule": rule.name}, "name"
                )
            )

            date_valid = (
                not rule.valid_from
                or getdate(args_copy.transaction_date) >= getdate(rule.valid_from)
            ) and (
                not rule.valid_upto
                or getdate(args_copy.transaction_date) <= getdate(rule.valid_upto)
            )

            filtered_rules = filter_pricing_rules_for_qty_amount(
                qty, amount, [rule], args_copy
            )
            qty_amt_valid = bool(filtered_rules)

            if (
                qty_amt_valid
                and coupon_valid
                and date_valid
                and not rule.get("suggestion")
            ):
                rule_details = get_pricing_rule_details(args_copy, rule)
                (coupon_rules if rule.coupon_code_based else rules).append(rule_details)
            else:
                suggestion_msg = inno_validate_quantity_and_amount_for_suggestion(
                    rule,
                    qty,
                    amount,
                    args_copy.get("item_code"),
                    args_copy.get("transaction_type"),
                )
                if suggestion_msg:
                    suggestions.append(
                        frappe._dict(
                            {
                                "name": rule.name,
                                "title": rule.title,
                                "suggestion_message": suggestion_msg,
                                "missing_qty": rule.min_qty - qty
                                if qty < rule.min_qty
                                else 0,
                                "missing_amount": rule.min_amt - amount
                                if amount < rule.min_amt
                                else 0,
                            }
                        )
                    )
                else:
                    reason = (
                        (
                            "Quantity (qty={0}) does not meet min_qty={1} or max_qty={2}"
                            if not qty_amt_valid
                            else "Coupon code {0} is invalid or missing"
                            if not coupon_valid
                            else "Transaction date {0} is outside valid period"
                        ).format(qty, rule.min_qty, rule.max_qty)
                        if not qty_amt_valid
                        else (args_copy.coupon_code or "missing")
                        if not coupon_valid
                        else (args_copy.transaction_date)
                    )
                    non_applicable.append(
                        frappe._dict(
                            {
                                "name": rule.name,
                                "title": rule.title,
                                "reason": reason,
                            }
                        )
                    )

        item_details.update(
            {
                "pricing_rules_list": [
                    frappe._dict(
                        {
                            "pricing_rule": r.pricing_rule,
                            "rate_or_discount": r.rate_or_discount,
                            "margin_type": r.margin_type,
                            "item_code": r.item_code,
                            "child_docname": r.child_docname,
                            "details": frappe.get_cached_doc(
                                "Pricing Rule", r.pricing_rule
                            ),
                        }
                    )
                    for r in rules
                ],
                "coupon_pricing_rules": [
                    frappe._dict(
                        {
                            "pricing_rule": r.pricing_rule,
                            "rate_or_discount": r.rate_or_discount,
                            "margin_type": r.margin_type,
                            "item_code": r.item_code,
                            "child_docname": r.child_docname,
                            "details": frappe.get_cached_doc(
                                "Pricing Rule", r.pricing_rule
                            ),
                        }
                    )
                    for r in coupon_rules
                ],
                "suggestion_rules": suggestions,
                "non_applicable_rules": non_applicable,
            }
        )
        out.append(item_details)

    return out


@frappe.whitelist(methods=["POST"])
def get_all_pricing_rules_for_transaction(args, doc=None):
    args = frappe._dict(json.loads(args) if isinstance(args, str) else args)
    doc = frappe.get_doc(json.loads(doc)) if isinstance(doc, str) else doc

    if not args.get("transaction_type"):
        set_transaction_type(args)
    if not args.get("transaction_date"):
        args.transaction_date = today()

    total_qty = flt(doc.total_qty if doc else args.get("total_qty", 0))
    total_amount = flt(doc.total if doc else args.get("total", 0))
    currency = doc.currency if doc else args.get("currency", "VND")

    output = frappe._dict(
        {"pricing_rules_list": [], "coupon_pricing_rules": [], "suggestion_rules": []}
    )

    conditions = "apply_on = 'Transaction'"
    values = {}
    conditions = get_other_conditions(conditions, values, args)

    pricing_rules = (
        frappe.db.sql(
            f"""SELECT `tabPricing Rule`.* FROM `tabPricing Rule`
        WHERE {conditions} AND `tabPricing Rule`.disable = 0""",
            values,
            as_dict=1,
        )
        or []
    )

    if not pricing_rules:
        return output

    pricing_rules = filter_pricing_rules_for_qty_amount(
        total_qty, total_amount, pricing_rules
    )
    pricing_rules = filter_pricing_rule_based_on_condition(pricing_rules, doc)

    for rule in pricing_rules:
        if isinstance(rule, str):
            rule = frappe.get_cached_doc("Pricing Rule", rule)

        date_valid = (
            not rule.valid_from
            or getdate(args.transaction_date) >= getdate(rule.valid_from)
        ) and (
            not rule.valid_upto
            or getdate(args.transaction_date) <= getdate(rule.valid_upto)
        )

        current_qty = total_qty
        current_amount = total_amount
        if rule.is_cumulative:
            data = get_qty_amount_data_for_cumulative(rule, doc or args, items=None)
            if data:
                current_qty += data[0]
                current_amount += data[1]

        qty_valid = current_qty >= flt(rule.min_qty) and (
            not rule.max_qty or current_qty <= flt(rule.max_qty)
        )
        amt_valid = current_amount >= flt(rule.min_amt) and (
            not rule.max_amt or current_amount <= flt(rule.max_amt)
        )

        if qty_valid and amt_valid and date_valid and not rule.get("suggestion"):
            rule_details = frappe._dict(
                {
                    "pricing_rule": rule.name,
                    "title": rule.title,
                    "rate_or_discount": rule.rate_or_discount,
                    "apply_discount_on": rule.apply_discount_on,
                    "details": rule,
                }
            )

            if rule.price_or_product_discount == "Product" and flt(rule.free_qty) > 0:
                rule_details["free_item_data"] = frappe._dict(
                    {
                        "item_code": rule.free_item,
                        "qty": flt(rule.free_qty),
                        "pricing_rules": rule.name,
                        "rate": flt(rule.free_item_rate),
                        "price_list_rate": 0.0,
                        "is_free_item": 1,
                        "item_name": frappe.get_cached_value(
                            "Item", rule.free_item, "item_name"
                        ),
                        "description": frappe.get_cached_value(
                            "Item", rule.free_item, "description"
                        ),
                        "stock_uom": frappe.get_cached_value(
                            "Item", rule.free_item, "stock_uom"
                        ),
                        "uom": rule.free_item_uom
                        or frappe.get_cached_value("Item", rule.free_item, "stock_uom"),
                        "conversion_factor": 1.0,
                    }
                )

            (
                output.coupon_pricing_rules
                if rule.coupon_code_based
                else output.pricing_rules_list
            ).append(rule_details)

        elif rule.get("threshold_percentage"):
            for field, value in {
                "min_qty": current_qty,
                "min_amt": current_amount,
                "max_qty": current_qty,
                "max_amt": current_amount,
            }.items():
                if rule.get(field) and (
                    (
                        value < rule.get(field)
                        and rule.get(field)
                        - cint(rule.get(field) * rule.threshold_percentage * 0.01)
                        <= value
                    )
                    or (
                        value > rule.get(field)
                        and rule.get(field)
                        + cint(rule.get(field) * rule.threshold_percentage * 0.01)
                        >= value
                    )
                ):
                    type_of_transaction = (
                        "sell" if args.transaction_type == "selling" else "buy"
                    )
                    suggestion_msg = _(
                        "If you {0} {1} {2}in total, the scheme {3} will be applied."
                    ).format(
                        type_of_transaction,
                        frappe.utils.fmt_money(rule.get(field), currency=currency)
                        if "amt" in field
                        else rule.get(field),
                        "worth " if "amt" in field else "",
                        rule.title,
                    )
                    output.suggestion_rules.append(
                        frappe._dict(
                            {
                                "name": rule.name,
                                "title": rule.title,
                                "suggestion_message": suggestion_msg,
                                "missing_qty": rule.min_qty - current_qty
                                if field == "min_qty"
                                else 0,
                                "missing_amount": rule.min_amt - current_amount
                                if field == "min_amt"
                                else 0,
                                "excess_qty": current_qty - rule.max_qty
                                if field == "max_qty"
                                else 0,
                                "excess_amount": current_amount - rule.max_amt
                                if field == "max_amt"
                                else 0,
                            }
                        )
                    )
                    break

    return output


def inno_apply_price_discount_rule(pricing_rule, item_details, args):
    item_details.pricing_rule_for = pricing_rule.rate_or_discount

    if (
        pricing_rule.margin_type in ["Amount", "Percentage"]
        and pricing_rule.currency == args.currency
    ) or (pricing_rule.margin_type == "Percentage"):
        item_details.margin_type = pricing_rule.margin_type
        item_details.has_margin = True

        if (
            pricing_rule.apply_multiple_pricing_rules
            and item_details.margin_rate_or_amount is not None
        ):
            item_details.margin_rate_or_amount += pricing_rule.margin_rate_or_amount
        else:
            item_details.margin_rate_or_amount = pricing_rule.margin_rate_or_amount

    if pricing_rule.rate_or_discount == "Rate":
        pricing_rule_rate = 0.0
        if pricing_rule.currency == args.currency:
            pricing_rule_rate = pricing_rule.rate

        if pricing_rule_rate:
            is_blank_uom = pricing_rule.get("uom") != args.get("uom")
            item_details.update(
                {
                    "price_list_rate": pricing_rule_rate
                    * (args.get("conversion_factor", 1) if is_blank_uom else 1),
                }
            )
        item_details.update({"discount_percentage": 0.0})

    for apply_on in ["Discount Amount", "Discount Percentage"]:
        if pricing_rule.rate_or_discount != apply_on:
            continue

        field = frappe.scrub(apply_on)
        if pricing_rule.apply_discount_on_rate and item_details.get(
            "discount_percentage"
        ):
            item_details[field] += (100 - item_details[field]) * (
                pricing_rule.get(field, 0) / 100
            )
            item_details["discount_amount"] = flt(
                flt(args.price_list_rate)
                * flt(item_details["discount_percentage"])
                / 100
            )

        elif pricing_rule.apply_discount_on_rate and item_details.get(
            "discount_amount"
        ):
            discount_percentage = (
                1
                - (
                    flt(
                        (flt(args.price_list_rate) - flt(item_details.discount_amount))
                        / flt(args.price_list_rate)
                    )
                )
            ) * 100
            item_details.discount_percentage = discount_percentage
            item_details[field] += (100 - item_details[field]) * (
                pricing_rule.get(field, 0) / 100
            )
            item_details["discount_amount"] = flt(
                flt(args.price_list_rate)
                * flt(item_details["discount_percentage"])
                / 100
            )
        elif args.price_list_rate:
            if (
                args.price_list_rate != item_details.price_list_rate
                and item_details.get("price_list_rate")
            ):
                args.price_list_rate = item_details.price_list_rate
            value = pricing_rule.get(field, 0)
            calculate_discount_percentage = False
            if field == "discount_percentage":
                field = "discount_amount"
                value = args.price_list_rate * (value / 100)
                calculate_discount_percentage = True

            if field not in item_details:
                item_details.setdefault(field, 0)

            item_details[field] += value if pricing_rule else args.get(field, 0)
            if (
                calculate_discount_percentage
                and args.price_list_rate
                and item_details.discount_amount
            ):
                item_details.discount_percentage = flt(
                    (flt(item_details.discount_amount) / flt(args.price_list_rate))
                    * 100
                )

        else:
            if field not in item_details:
                item_details.setdefault(field, 0)

            item_details[field] += (
                pricing_rule.get(field, 0) if pricing_rule else args.get(field, 0)
            )

    if (
        item_details.get("discount_amount")
        and item_details.discount_amount > args.price_list_rate
    ):
        item_details.discount_amount = args.price_list_rate

        if args.price_list_rate > 0:
            item_details.discount_percentage = flt(
                (item_details.discount_amount / args.price_list_rate) * 100
            )


pricing_rule.apply_price_discount_rule = inno_apply_price_discount_rule


@frappe.whitelist(methods=["POST"])
def inno_remove_pricing_rule_for_item(
    pricing_rules, item_details, item_code=None, rate=None
):
    from erpnext.accounts.doctype.pricing_rule.utils import (
        get_pricing_rule_items,
    )

    if isinstance(item_details, str):
        item_details = json.loads(item_details)
        item_details = frappe._dict(item_details)

    for d in get_applied_pricing_rules(pricing_rules):
        if not d or not frappe.db.exists("Pricing Rule", d):
            continue
        pricing_rule = frappe.get_cached_doc("Pricing Rule", d)

        if pricing_rule.price_or_product_discount == "Price":
            if pricing_rule.rate_or_discount == "Discount Percentage":
                item_details.discount_percentage = 0.0
                item_details.discount_amount = 0.0
                item_details.rate = rate or 0.0
            if pricing_rule.rate_or_discount == "Discount Amount":
                item_details.discount_amount = 0.0
                item_details.rate = rate or 0.0
                item_details.discount_percentage = 0.0

            if pricing_rule.margin_type in ["Percentage", "Amount"]:
                item_details.margin_rate_or_amount = 0.0
                item_details.margin_type = None
        elif pricing_rule.get("free_item") and not pricing_rule.get(
            "dont_enforce_free_item_qty"
        ):
            item_details.remove_free_item = (
                item_code
                if pricing_rule.get("same_item")
                else pricing_rule.get("free_item")
            )

        if pricing_rule.get("mixed_conditions") or pricing_rule.get(
            "apply_rule_on_other"
        ):
            items = get_pricing_rule_items(pricing_rule, other_items=True)
            item_details.apply_on = (
                frappe.scrub(pricing_rule.apply_rule_on_other)
                if pricing_rule.apply_rule_on_other
                else frappe.scrub(pricing_rule.get("apply_on"))
            )
            item_details.applied_on_items = ",".join(items)

    item_details.pricing_rules = ""
    item_details.pricing_rule_removed = True

    return item_details


pricing_rule.remove_pricing_rule_for_item = inno_remove_pricing_rule_for_item


@frappe.whitelist(methods=["POST"])
def inno_apply_transaction_pricing_rule(pricing_rule=None, doc=None):
    out = {
        "additional_discount_percentage": 0.0,
        "discount_amount": 0.0,
        "free_item_data": [],
        "applied_pricing_rules": "",
        "coupon_pricing_rule_discount_percentage": 0.0,
        "coupon_pricing_rule_discount_amount": 0.0,
    }

    if isinstance(doc, str):
        doc = json.loads(doc)
    if doc:
        doc = frappe.get_doc(doc)

    total = flt(getattr(doc, "total", 0.0), 2) if doc else 0.0
    if total < 0:
        total = 0.0

    rules = []
    try:
        if pricing_rule:
            rule_doc = frappe.get_cached_doc("Pricing Rule", pricing_rule)
            if rule_doc.apply_on == "Transaction":
                rules.append(rule_doc)

        if doc and hasattr(doc, "coupon_code") and doc.coupon_code:
            coupon_code = doc.coupon_code
            coupon_pricing_rule = frappe.db.get_value(
                doctype="Coupon Code",
                filters={"name": coupon_code},
                fieldname="pricing_rule",
            )
            if coupon_pricing_rule:
                coupon_rule_doc = frappe.get_cached_doc(
                    "Pricing Rule", coupon_pricing_rule
                )
                if (
                    coupon_rule_doc.apply_on == "Transaction"
                    and coupon_rule_doc not in rules
                ):
                    rules.append(coupon_rule_doc)

    except frappe.DoesNotExistError:
        frappe.msgprint(
            {
                "title": _("Error"),
                "message": _(
                    "[Unverified] One or more pricing rules or coupon codes do not exist."
                ),
                "indicator": "red",
            }
        )
        return out

    remaining_total = total

    for rule in rules:
        if not rule:
            continue

        date_valid = True
        transaction_date = getattr(doc, "transaction_date", None) if doc else None
        posting_date = getattr(doc, "posting_date", None) if doc else None
        current_date = transaction_date or posting_date or today()

        if rule.valid_from and getdate(current_date) < getdate(rule.valid_from):
            date_valid = False
        if rule.valid_upto and getdate(current_date) > getdate(rule.valid_upto):
            date_valid = False

        if not date_valid:
            continue

        if rule.price_or_product_discount == "Price":
            field = frappe.scrub(rule.rate_or_discount)

            if field not in out:
                out[field] = 0.0

            if rule.rate_or_discount == "Discount Amount" and rule.discount_amount > 0:
                discount_amount = flt(rule.discount_amount, 2)
                out["discount_amount"] += discount_amount
                remaining_total -= discount_amount
                if len(rules) > 1:
                    out["additional_discount_percentage"] = (
                        flt((out["discount_amount"] / total) * 100, 3)
                        if total > 0
                        else 0.0
                    )
                if (
                    doc
                    and hasattr(doc, "coupon_code")
                    and doc.coupon_code
                    and rule.name == coupon_pricing_rule
                ):
                    out["coupon_pricing_rule_discount_amount"] = discount_amount
                    out["coupon_pricing_rule_discount_percentage"] = (
                        flt((discount_amount / total) * 100, 3) if total > 0 else 0.0
                    )

            elif (
                rule.rate_or_discount == "Discount Percentage"
                and rule.discount_percentage > 0
            ):
                if rule.apply_discount_on_rate:
                    discount_amount = flt(
                        remaining_total * rule.discount_percentage / 100, 2
                    )
                    out["discount_amount"] += discount_amount
                    remaining_total -= discount_amount
                    out["additional_discount_percentage"] = (
                        flt((out["discount_amount"] / total) * 100, 3)
                        if total > 0
                        else 0.0
                    )
                else:
                    out["additional_discount_percentage"] += flt(
                        rule.discount_percentage
                    )
                    discount_amount = flt(total * rule.discount_percentage / 100, 2)
                    out["discount_amount"] += discount_amount
                    remaining_total -= discount_amount
                if (
                    doc
                    and hasattr(doc, "coupon_code")
                    and doc.coupon_code
                    and rule.name == coupon_pricing_rule
                ):
                    out["coupon_pricing_rule_discount_percentage"] = flt(
                        rule.discount_percentage, 3
                    )
                    out["coupon_pricing_rule_discount_amount"] = discount_amount

        elif rule.price_or_product_discount == "Product" and rule.free_item:
            qty = flt(rule.free_qty, rule.precision("free_qty"))
            if qty <= 0:
                qty = 1.0

            try:
                item_doc = frappe.get_cached_doc("Item", rule.free_item)
                free_item_data = {
                    "item_code": item_doc.item_code,
                    "item_name": item_doc.item_name,
                    "description": item_doc.description,
                    "qty": qty,
                    "uom": item_doc.stock_uom,
                    "stock_uom": item_doc.stock_uom,
                    "conversion_factor": 1.0,
                    "is_free_item": 1,
                    "rate": 0.0,
                    "price_list_rate": 0.0,
                    "discount_percentage": 0.0,
                    "discount_amount": 0.0,
                }

                delivery_date = getattr(doc, "delivery_date", None) if doc else None
                transaction_date = (
                    getattr(doc, "transaction_date", None) if doc else None
                )
                posting_date = getattr(doc, "posting_date", None) if doc else None
                if delivery_date or transaction_date or posting_date:
                    free_item_data["delivery_date"] = (
                        delivery_date or transaction_date or posting_date
                    )
                out["free_item_data"].append(free_item_data)
            except frappe.DoesNotExistError:
                frappe.msgprint(
                    {
                        "title": _("Error"),
                        "message": _(
                            "[Unverified] Free item {} does not exist."
                        ).format(rule.free_item),
                        "indicator": "red",
                    }
                )

    if total > 0 and out["discount_amount"] > total:
        out["discount_amount"] = total
        out["additional_discount_percentage"] = flt(
            (out["discount_amount"] / total) * 100
        )

    out["discount_amount"] = flt(out["discount_amount"])

    applied_rules = [r.name for r in rules if r]
    out["applied_pricing_rules"] = json.dumps(applied_rules) if applied_rules else ""

    return out
