# Copyright (c) 2025, Tada Labs and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class PaymentSetting(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		payoo_account_name: DF.Data | None
		payoo_create_shop_code: DF.Data | None
		payoo_credential_plain: DF.Password | None
		payoo_enable: DF.Check
		payoo_order_link_notify: DF.Data | None
		payoo_private_key_path: DF.Attach | None
		payoo_public_key_path: DF.Attach | None
		payoo_username: DF.Data | None
	# end: auto-generated types
	pass

	def before_save(self):
		exists_payoo = frappe.db.exists("Mode of Payment", "Payoo")
		if self.payoo_enable:
			if not exists_payoo:
				payoo_mop = frappe.new_doc("Mode of Payment")
				payoo_mop.mode_of_payment = "Payoo"
				payoo_mop.enabled = 1
				payoo_mop.type = "Bank"
				payoo_mop.append(
					"accounts",
					{
						"company": frappe.get_cached_value("Company", None, "default_company"),
						"default_account": frappe.db.get_value("Account", {"account_number": "1121"}, "name"),
					},
				)
				payoo_mop.insert()
			else:
				payoo_mode = frappe.get_doc("Mode of Payment", {"mode_of_payment": "Payoo"})
				payoo_mode.enabled = 1
				payoo_mode.save()
		else:
			if exists_payoo:
				payoo_mode = frappe.get_doc("Mode of Payment", {"mode_of_payment": "Payoo"})
				payoo_mode.enabled = 0
				payoo_mode.save()
