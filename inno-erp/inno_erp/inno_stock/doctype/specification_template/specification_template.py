# Copyright (c) 2025, TadaLabs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class SpecificationTemplate(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from inno_erp.inno_stock.doctype.has_item_group.has_item_group import HasItemGroup
		from inno_erp.inno_stock.doctype.specifications.specifications import Specifications

		item_groups: DF.TableMultiSelect[HasItemGroup]
		name_template: DF.Data
		spec_item: DF.Table[Specifications]
	# end: auto-generated types

	pass
