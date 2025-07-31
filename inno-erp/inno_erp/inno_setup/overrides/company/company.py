import frappe
from erpnext.setup.doctype.company.company import Company
from frappe import _

from inno_erp.inno_account.overrides.account.chart_of_accounts import (
	standard_200_coa_vietnam,
)


class InnoCompany(Company):
	def create_default_accounts(self):
		if self.chart_of_accounts != "Standard 200 COA Vietnam":
			return super().create_default_accounts()

		from erpnext.accounts.doctype.account.chart_of_accounts.chart_of_accounts import (
			create_charts,
		)

		frappe.local.flags.ignore_root_company_validation = True
		create_charts(
			self.name,
			self.chart_of_accounts,
			self.existing_company,
			standard_200_coa_vietnam.get(),
		)

		self.db_set(
			"default_receivable_account",
			frappe.db.get_value(
				"Account",
				{"company": self.name, "account_type": "Receivable", "is_group": 0},
			),
		)

		self.db_set(
			"default_payable_account",
			frappe.db.get_value(
				"Account",
				{"company": self.name, "account_type": "Payable", "is_group": 0},
			),
		)

		self.db_set(
			"write_off_account",
			frappe.db.get_value(
				"Account",
				{"company": self.name, "account_type": "Round Off", "is_group": 0},
			),
		)

		default_settings = {
			"default_discount_account": "5211",
			"default_deferred_revenue_account": "3387",
			"default_deferred_expense_account": "242",
			"default_expense_claim_payable_account": "3341",
			"default_payroll_payable_account": "3341",
			"default_employee_advance_account": "141",
			"stock_received_but_not_billed": "335",
		}

		for key, value in default_settings.items():
			self.db_set(
				key,
				frappe.db.get_value(
					"Account",
					{"company": self.name, "account_number": value, "is_group": 0},
				),
			)

	def create_default_warehouses(self):
		parent_warehouse = None
		for wh_detail in [
			{"warehouse_name": _("All Warehouses"), "is_group": 1},
			{"warehouse_name": _("Stores"), "is_group": 0},
			{"warehouse_name": _("Goods In Transit"), "is_group": 0, "warehouse_type": "Transit"},
		]:
			if frappe.db.exists(
				"Warehouse",
				{
					"warehouse_name": wh_detail["warehouse_name"],
					"company": self.name,
				},
			):
				continue

			warehouse = frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": wh_detail["warehouse_name"],
					"is_group": wh_detail["is_group"],
					"company": self.name,
					"parent_warehouse": parent_warehouse,
					"warehouse_type": wh_detail.get("warehouse_type"),
				}
			)
			warehouse.flags.ignore_permissions = True
			warehouse.flags.ignore_mandatory = True
			warehouse.insert()

			if wh_detail["is_group"]:
				parent_warehouse = warehouse.name
