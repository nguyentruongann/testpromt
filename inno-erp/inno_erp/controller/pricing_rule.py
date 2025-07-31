import frappe
from frappe import _

from inno_erp.inno_account.overrides.pricing_rule.pricing_rule import (
    get_all_pricing_rules_for_item,
    get_all_pricing_rules_for_transaction,
)


@frappe.whitelist(methods=["POST"])
def validate_coupon_code(args):
    if isinstance(args, str):
        args = frappe.parse_json(args)
    args = frappe._dict(args)
    coupon_code = args.get("coupon_code")

    if not coupon_code or not isinstance(coupon_code, str) or not coupon_code.strip():
        return {"valid": False, "message": _("Coupon code is required or invalid.")}

    try:
        # Kiểm tra schema của Coupon Code
        if not frappe.db.exists("DocType", "Coupon Code"):
            return {
                "valid": False,
                "message": _("[Unverified] Coupon Code doctype does not exist."),
            }

        # Kiểm tra các field cần thiết
        required_fields = ["pricing_rule", "custom_disable"]
        field_list = frappe.get_meta("Coupon Code").get_valid_columns()
        missing_fields = [f for f in required_fields if f not in field_list]
        if missing_fields:
            return {
                "valid": False,
                "message": _("[Unverified] Missing fields in Coupon Code: {0}").format(
                    ", ".join(missing_fields)
                ),
            }

        # Truy vấn coupon code với field disable
        coupon_data = frappe.db.get_value(
            "Coupon Code", coupon_code, ["pricing_rule", "custom_disable"], as_dict=True
        )
        if not coupon_data:
            return {
                "valid": False,
                "message": _(f"Coupon code {coupon_code} does not exist."),
            }
        if coupon_data.custom_disable:
            return {"valid": False, "message": _("Coupon code is disabled.")}
        coupon_pricing_rule = coupon_data.pricing_rule
        if not coupon_pricing_rule:
            return {
                "valid": False,
                "message": _(f"Coupon code {coupon_code} is invalid."),
            }

        doctype = args.get("doctype", "Sales Order")
        doc = frappe._dict(
            {
                "doctype": doctype,
                "currency": args.get("currency", "VND"),
                "conversion_rate": args.get("conversion_rate", 1.0),
                "selling_price_list": args.get("price_list"),
            }
        )

        transaction_date = (
            args.get("transaction_date")
            or args.get("posting_date")
            or frappe.utils.nowdate()
        )
        validation_args = {
            "doctype": doctype,
            "company": args.get("company"),
            "customer": args.get("customer"),
            "currency": doc.currency,
            "conversion_rate": doc.conversion_rate,
            "price_list": doc.selling_price_list,
            "transaction_date": transaction_date,
            "coupon_code": coupon_code,
            "items": args.get("items", []),
            "total": args.get("total", 0.0),
            "total_qty": args.get("total_qty", 0.0),
        }

        pr_doc = frappe.get_doc("Pricing Rule", coupon_pricing_rule)

        item_codes = [item.item_code for item in pr_doc.get("items", [])]
        item_groups = [group.item_group for group in pr_doc.get("item_groups", [])]
        brands = [brand.brand for brand in pr_doc.get("brands", [])]
        is_transaction_level = not (item_codes or item_groups or brands)

        def get_applicable_message():
            parts = []
            if item_codes:
                parts.append(f"items: {', '.join(item_codes)}")
            if item_groups:
                parts.append(f"item groups: {', '.join(item_groups)}")
            if brands:
                parts.append(f"brands: {', '.join(brands)}")
            return (
                f"Coupon is only applicable for {' and '.join(parts)}"
                if parts
                else "Coupon is not applicable for any items in the order."
            )

        if is_transaction_level:
            transaction_result = get_all_pricing_rules_for_transaction(
                {
                    "transaction_type": "selling",
                    "transaction_date": transaction_date,
                    "company": validation_args["company"],
                    "customer": validation_args["customer"],
                    "doctype": doctype,
                    "total_qty": validation_args["total_qty"],
                    "total": validation_args["total"],
                    "coupon_code": coupon_code,
                }
            )
            applicable_pricing_rules = [
                rule["details"]["name"]
                for rule in transaction_result.get("coupon_pricing_rules", [])
            ]
            if coupon_pricing_rule not in applicable_pricing_rules:
                return {
                    "valid": False,
                    "message": _("Coupon is not applicable for this transaction."),
                }
        else:
            if not validation_args["items"]:
                return {"valid": False, "message": get_applicable_message()}
            item_result = get_all_pricing_rules_for_item(validation_args, doc=doc)
            applicable_pricing_rules = []
            for item_data in item_result:
                applicable_pricing_rules.extend(
                    [
                        rule["pricing_rule"]
                        for rule in item_data.get("pricing_rules_list", [])
                    ]
                    + [
                        rule["pricing_rule"]
                        for rule in item_data.get("coupon_pricing_rules", [])
                    ]
                )
            if coupon_pricing_rule not in applicable_pricing_rules:
                return {"valid": False, "message": get_applicable_message()}

        return {
            "valid": True,
            "pricing_rule": coupon_pricing_rule,
            "applicable": {
                "item_codes": item_codes,
                "item_groups": item_groups,
                "brands": brands,
            },
            "is_transaction_level": is_transaction_level,
        }

    except frappe.DoesNotExistError:
        return {
            "valid": False,
            "message": _(f"Pricing rule {coupon_pricing_rule} does not exist."),
        }
    except Exception as e:
        frappe.log_error(f"Error validating coupon code {coupon_code}: {str(e)}")
        return {
            "valid": False,
            "message": _(
                "[Unverified] An error occurred while validating the coupon code."
            ),
        }
