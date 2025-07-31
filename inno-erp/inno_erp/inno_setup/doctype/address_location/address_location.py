# Copyright (c) 2025, TadaLabs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AddressLocation(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		country: DF.Link
		district_code: DF.Data
		province_district: DF.Data
	# end: auto-generated types
	pass
