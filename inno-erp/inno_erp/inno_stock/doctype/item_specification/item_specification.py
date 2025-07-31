# Copyright (c) 2025, TadaLabs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ItemSpecification(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		name: DF.Int | None
		parent: DF.Data
		parentfield: DF.Data
		parenttype: DF.Data
		spec_name: DF.Data
		spec_value: DF.Data | None
	# end: auto-generated types

	pass
