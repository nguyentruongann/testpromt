# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SellingSetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from inno_erp.inno_selling.doctype.refund_rule.refund_rule import RefundRule

		allow_return_promotion_product: DF.Check
		allow_trade_with_lower_value: DF.Check
		refund_rule: DF.Table[RefundRule]
	# end: auto-generated types
	pass
