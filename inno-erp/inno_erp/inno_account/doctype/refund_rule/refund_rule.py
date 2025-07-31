# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class RefundRule(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		refund_percent: DF.Data | None
		refund_time: DF.Data | None
	# end: auto-generated types
	pass
