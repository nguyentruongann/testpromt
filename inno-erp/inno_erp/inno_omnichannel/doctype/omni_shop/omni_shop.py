# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class OmniShop(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		credentials: DF.Password | None
		disabled: DF.Check
		image: DF.AttachImage | None
		last_sync: DF.Datetime | None
		naming_series: DF.Literal["OMNI-"]
		platform: DF.Literal["Lazada", "Tiktok Shop", "Shopee"]
		seller_id: DF.Data | None
		shop_id: DF.Data | None
		shop_name: DF.Data | None
		sync_status: DF.Literal["", "Pending", "Failed", "Success"]
	# end: auto-generated types
	pass
