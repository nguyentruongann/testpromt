# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class LoyaltyProgramSpecialDay(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		active: DF.Check
		date: DF.Date | None
		day_name: DF.Link
		description: DF.Text | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		rate: DF.Float
	# end: auto-generated types
	pass
