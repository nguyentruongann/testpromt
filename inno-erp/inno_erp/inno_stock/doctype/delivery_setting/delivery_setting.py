# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

from frappe import _
from frappe.model.document import Document

PROVIDERS = ["GHTK", "GHN", "ViettelPost"]

DEFAULT_TYPE = "Sales"


class DeliverySetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		ghn_enable: DF.Check
		ghn_token: DF.Password | None
		ghtk_enable: DF.Check
		ghtk_token: DF.Password | None
		viettel_enable: DF.Check
		viettel_token: DF.Password | None
	# end: auto-generated types
	pass
