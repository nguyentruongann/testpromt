
from frappe.model.document import Document
from erpnext.accounts.doctype.coupon_code.coupon_code import CouponCode

import frappe
from frappe.model.document import Document
from enum import Enum

class ApplyOn(Enum):
    ITEM_CODE = "Item Code"
    ITEM_GROUP = "Item Group"
    BRAND = "Brand"

PRICING_RULE_CONFIG = {
    "scalar_fields": {
        # Apply On fields
        "disable": "custom_disable",
        "apply_on": "custom_apply_on",
        "price_or_product_discount": "custom_price_or_product_discount",
        "is_cumulative": "custom_is_cumulative",
        "mixed_conditions": "custom_mixed_conditions",
        "warehouse": "custom_warehouse",
         # Discount on Other Item fields
        "apply_rule_on_other": "custom_apply_rule_on_other",
        "other_item_code": "custom_item_code",
        "other_item_group": "custom_item_group",
        "other_brand": "custom_brand",
        # Party Information fields
        "applicable_for": "custom_applicable_for",
        "customer": "custom_customer_applicable",
        "customer_group": "custom_customer_group",
        "territory": "custom_territory",
        "sales_partner": "custom_sales_partner",
        "campaign": "custom_campaign",
        "supplier": "custom_supplier",
        "supplier_group": "custom_supplier_group",
        #Quantity and Amount fields
        "min_qty": "custom_min_qty_as_per_stock_uom",
        "max_qty": "custom_max_qty_as_per_stock_uom",
        "min_amt": "custom_min_amt",
        "max_amt": "custom_max_amt",
        # Period Settings fields
        "valid_from": "custom_valid_from_pricing_rule",
        "valid_upto": "custom_valid_upto_pricing_rule",
        "company": "custom_company",
        "currency": "custom_currency",
        #Margin
        "margin_type": "custom_margin_type",
        "margin_rate_or_amount": "custom_margin_rate_or_amount",
        # Price Discount Scheme fields
        "rate_or_discount": "custom_rate_or_discount",
        "apply_discount_on": "custom_apply_discount_on",
        "rate": "custom_rate",
        "discount_amount": "custom_discount_amount",
        "discount_percentage": "custom_discount_percentage",
        "for_price_list": "custom_for_price_list",
        # Product discount scheme
        "free_item": "custom_free_item",
        "same_item": "custom_same_item",
        "free_qty": "custom_qty",
        "free_item_rate": "custom_free_item_rate",
        "free_item_uom": "custom_uom",
        "round_free_qty": "custom_round_free_qty",
        "dont_enforce_free_item_qty": "custom_dont_enforce_free_item_qty",
        "is_recursive": "custom_is_recursive",
        "recurse_for": "custom_recurse_every_as_per_transaction_uom",
        "apply_recursion_over": "custom_apply_recursion_over_as_per_transaction_uom",
    },
    "table_fields": {
        "items": {
            "custom_field": "custom_pricing_rule_item_code",
            "comparison_fields": ["item_code", "uom"],
            "apply_on": ApplyOn.ITEM_CODE.value
        },
        "item_groups": {
            "custom_field": "custom_pricing_rule_item_group",
            "comparison_fields": ["item_group", "uom"],
            "apply_on": ApplyOn.ITEM_GROUP.value
        },
        "brands": {
            "custom_field": "custom_pricing_rule_brand",
            "comparison_fields": ["brand", "uom"],
            "apply_on": ApplyOn.BRAND.value
        }
    }
}

class InnoCouponCode(CouponCode):
    
    def after_insert(self):
        self.fill_pricing_rule_data(self.pricing_rule)
        try:
            pricing_rule = frappe.get_doc("Pricing Rule", self.pricing_rule)
            pricing_rule.custom_coupon_code = self.name
            pricing_rule.save()
        except Exception as e:
            # use enlish
            frappe.log_error(frappe.get_traceback(), "Error updating Pricing Rule")
            frappe.throw(f"Error updating Pricing Rule")
        

    def before_save(self):
        if self.pricing_rule:
            self._sync_to_pricing_rule()
        if not self.pricing_rule and self.is_new():
            self._create_pricing_rule_from_custom_fields()
        
    def _create_pricing_rule_from_custom_fields(self):
        try:
            pricing_rule = frappe.new_doc("Pricing Rule")
            
            for original_field, custom_field in PRICING_RULE_CONFIG["scalar_fields"].items():
                custom_value = getattr(self, custom_field, None)
                if custom_value is not None:
                    setattr(pricing_rule, original_field, custom_value)

            self.set_pricing_rule(pricing_rule)
            self._set_table_fields_based_on_apply_on(pricing_rule)
            
            pricing_rule.insert()
            frappe.db.commit()
            
            self.pricing_rule = pricing_rule.name
        except Exception as e:
            frappe.throw(f"Error creating Pricing Rule")
            
    def set_pricing_rule(self, pricing_rule_name):
        pricing_rule_name.coupon_code_based = 1
        pricing_rule_name.selling = 1
        pricing_rule_name.title = self.coupon_name
        pricing_rule_name.apply_multiple_pricing_rules = 1
        pricing_rule_name.apply_discount_on_rate = 1
        pricing_rule_name.has_priority = 1
        pricing_rule_name.priority = "2"

    def _sync_to_pricing_rule(self):
        try:
            pricing_rule = frappe.get_doc("Pricing Rule", self.pricing_rule)
            has_changes = False

            for original_field, custom_field in PRICING_RULE_CONFIG["scalar_fields"].items():
                custom_value = getattr(self, custom_field)
                pricing_value = getattr(pricing_rule, original_field)
                if custom_value != pricing_value:
                    setattr(pricing_rule, original_field, custom_value)
                    has_changes = True
                        
            has_changes |= self._set_table_fields_based_on_apply_on(pricing_rule)
            if has_changes:
                pricing_rule.save()

        except Exception as e:
            frappe.throw(f"Error syncing with Pricing Rule")

    def _set_table_fields_based_on_apply_on(self, pricing_rule):
        has_changes = False
        apply_on = getattr(self, PRICING_RULE_CONFIG["scalar_fields"]["apply_on"], None)

        if not apply_on:
            return has_changes

        table_config = next(
            (config for config in PRICING_RULE_CONFIG["table_fields"].values() if config["apply_on"] == apply_on),
            None
        )
        if not table_config:
            return has_changes

        custom_field = table_config["custom_field"]
        target_field = next(
            (field for field, cfg in PRICING_RULE_CONFIG["table_fields"].items() if cfg["custom_field"] == custom_field),
            None
        )
        comparison_fields = table_config["comparison_fields"]

        custom_table = getattr(self, custom_field, []) or []
        pricing_table = getattr(pricing_rule, target_field, []) or []

        custom_rows = [{f: row.get(f) or "" for f in comparison_fields} for row in custom_table]
        pricing_rows = [{f: row.get(f) or "" for f in comparison_fields} for row in pricing_table]

        if custom_rows != pricing_rows:
            pricing_rule.set(target_field, [])
            for row in custom_table:
                new_row = {f: row.get(f) for f in comparison_fields}
                pricing_rule.append(target_field, new_row)
            has_changes = True

        return has_changes
    
    def fill_pricing_rule_data(self, pricing_rule_name):
        try:
            pricing_rule = frappe.get_doc("Pricing Rule", pricing_rule_name)
            result = {}
            
            for source_field, target_field in PRICING_RULE_CONFIG["scalar_fields"].items():
                source_value = getattr(pricing_rule, source_field, None)
                if source_value is not None:
                    result[target_field] = source_value
            
            for table_field, config in PRICING_RULE_CONFIG["table_fields"].items():
                if pricing_rule.get(table_field):
                    result[config["custom_field"]] = [
                        item.as_dict() for item in pricing_rule.get(table_field)
                    ]
            
            return result
            
        except Exception as e:
            return {}


    
