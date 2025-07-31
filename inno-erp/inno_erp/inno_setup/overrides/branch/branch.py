import frappe
from erpnext import get_default_company
from erpnext.setup.doctype.branch.branch import Branch
from frappe import _, msgprint
from frappe.model.naming import make_autoname, set_name_from_naming_options
from frappe.utils import cint, cstr

from inno_erp.utils.address import format_location, format_ward

BRANCH_APPLICABLE_FOR = {
	"Warehouse": [
		"Warehouse",
		"Stock Entry",
		"Purchase Receipt",
		"Material Request",
		"Purchase Order",
		"Purchase Invoice",
		"Sales Order",
		"Sales Invoice",
		"POS Profile",
		"POS Invoice",
	],
	"Cost Center": [
		"Cost Center",
		"Purchase Receipt",
		"Stock Entry",
		"Sales Order",
		"Sales Invoice",
		"POS Profile",
		"POS Invoice",
		"Purchase Order",
		"Purchase Invoice",
	],
	"Branch": [
		"Branch",
	],
}


POS_PROFILE_NAME = "{branch_name} - POS"
DEFAULT_WRITE_OFF_LIMIT = 1000


class InnoBranch(Branch):
	def autoname(self):
		branch_master_name = frappe.defaults.get_global_default("branch_master_name")
		if not branch_master_name or branch_master_name == "Branch Name":
			self.name = self.get_branch_name()
		elif branch_master_name == "Naming Series":
			self.name = make_autoname(self.custom_naming_series + ".#####", "", self)
		else:
			set_name_from_naming_options(frappe.get_meta(self.doctype).autoname, self)

	def get_branch_name(self):
		if frappe.db.get_value("Branch", self.branch) and not frappe.flags.in_import:
			count = frappe.db.sql(
				"""select ifnull(MAX(CAST(SUBSTRING_INDEX(name, ' ', -1) AS UNSIGNED)), 0) from tabBranch
                 where name like %s""",
				f"%{self.branch} - %",
				as_list=1,
			)[0][0]
			count = cint(count) + 1

			new_branch_name = f"{self.branch} - {cstr(count)}"

			msgprint(
				_("Changed branch name to '{}' as '{}' already exists.").format(new_branch_name, self.branch),
				title=_("Note"),
				indicator="yellow",
			)

			return new_branch_name

		return self.branch

	def validate(self):
		if not self.custom_address_line or not self.custom_address_location or not self.custom_ward:
			frappe.throw(_("Please fill in the Address Line, Location, and Ward for the branch"))

		province, district = format_location(self.custom_address_location)
		ward = format_ward(self.custom_ward)
		self.custom_address = f"{self.custom_address_line}, {ward}, {district}, {province}"

		if not self.custom_company:
			self.custom_company = get_default_company(frappe.session.user) or frappe.db.get_single_value(
				"Global Defaults", "default_company"
			)
			if not self.custom_company:
				frappe.throw(_("Please select a Company for the branch"))

	def after_insert(self):
		company = self.custom_company or get_default_company(frappe.session.user)
		suffix = " - " + frappe.get_cached_value("Company", company, "abbr")
		branch_with_suffix = self.branch + suffix if not self.branch.endswith(suffix) else self.branch

		if not frappe.db.exists("Cost Center", branch_with_suffix):
			cost_center = frappe.get_doc(
				{
					"doctype": "Cost Center",
					"cost_center_name": self.branch,
					"company": self.custom_company,
					"is_group": 0,
					"parent_cost_center": frappe.db.get_value(
						"Cost Center", {"is_group": 1, "company": self.custom_company}, "name"
					),
				}
			)
			cost_center.insert(ignore_permissions=True)
			self.custom_cost_center = cost_center.name

		parent_warehouse = frappe.db.get_value("Warehouse", {"lft": 1}, "name")

		if not frappe.db.exists("Warehouse", branch_with_suffix):
			warehouse = frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": self.branch,
					"company": self.custom_company,
					"is_group": 1,
					"parent_warehouse": parent_warehouse,
				}
			)
			warehouse.insert(ignore_permissions=True)

			self.custom_warehouse = warehouse.name
			child_warehouse = frappe.get_doc(
				{
					"doctype": "Warehouse",
					"warehouse_name": f"{self.branch} - {_('Sales')}",
					"warehouse_type": "Sales",
					"company": self.custom_company,
					"is_group": 0,
					"parent_warehouse": warehouse.name,
				}
			)
			child_warehouse.insert(ignore_permissions=True)
			self.custom_selling_warehouse = child_warehouse.name

		if not frappe.db.exists("POS Profile", POS_PROFILE_NAME.format(branch_name=self.branch)):
			self.create_new_pos_profile()

		self.db_update()
		frappe.db.commit()

	def on_update(self):
		if self.has_value_changed("custom_user_list"):
			new_users = [row.user for row in self.custom_user_list if row.user]

			old_doc = self.get_doc_before_save()
			if hasattr(old_doc, "custom_user_list"):
				old_users = [row.user for row in old_doc.custom_user_list if row.user]
			else:
				old_users = []

			removed_users = set(old_users) - set(new_users)
			added_users = set(new_users) - set(old_users)

			self.assign_user_permissions(added_users, removed_users)

	def assign_user_permissions(self, added_users, removed_users):
		try:
			warehouse = self.custom_warehouse
			cost_center = self.custom_cost_center
			branch = self.branch

			if removed_users and not self.is_new():
				frappe.db.delete(
					"User Permission",
					{"user": ("in", removed_users), "allow": "Warehouse", "for_value": warehouse},
				)
				frappe.db.delete(
					"User Permission",
					{"user": ("in", removed_users), "allow": "Cost Center", "for_value": cost_center},
				)
				frappe.db.delete(
					"User Permission",
					{"user": ("in", removed_users), "allow": "Branch", "for_value": branch},
				)

			if not added_users:
				return

			for user in added_users:
				for allow_doctype, applicable_for in BRANCH_APPLICABLE_FOR.items():
					if allow_doctype == "Warehouse":
						for_value = warehouse
					elif allow_doctype == "Cost Center":
						for_value = cost_center
					elif allow_doctype == "Branch":
						for_value = branch

					for doc_type in applicable_for:
						user_perm = frappe.get_doc(
							{
								"doctype": "User Permission",
								"user": user,
								"allow": allow_doctype,
								"for_value": for_value,
								"apply_to_all_doctypes": 0,
								"applicable_for": doc_type,
							}
						)
						user_perm.insert()

		except Exception as e:
			frappe.throw(_("Error assigning user permissions", e))

	def create_new_pos_profile(self):
		pos_profile_name = POS_PROFILE_NAME.format(branch_name=self.branch)
		default_company = frappe.get_doc("Company", get_default_company())

		cash_method = frappe.db.get_value("Mode of Payment", {"type": "Cash", "enabled": 1}, pluck="name")
		bank_method = frappe.db.get_value("Mode of Payment", {"type": "Bank", "enabled": 1}, pluck="name")

		payment_methods = []
		if cash_method:
			payment_methods.append({"mode_of_payment": cash_method, "default": 0})
		if bank_method:
			payment_methods.append({"mode_of_payment": bank_method, "default": 1})

		pos_profile = frappe.get_doc(
			{
				"doctype": "POS Profile",
				"pos_profile_name": pos_profile_name,
				"warehouse": self.custom_selling_warehouse,
				"company": self.custom_company,
				"payments": payment_methods,
				"validate_stock_on_save": 1,
				"print_receipt_on_order_complete": 1,
				"selling_price_list": frappe.db.get_single_value("Selling Settings", "selling_price_list"),
				"write_off_account": default_company.write_off_account,
				"write_off_limit": DEFAULT_WRITE_OFF_LIMIT,
				"write_off_cost_center": self.custom_cost_center,
				"cost_center": self.custom_cost_center,
				"income_account": default_company.default_income_account,
			}
		)
		pos_profile.name = pos_profile_name
		pos_profile.insert(ignore_permissions=True)

		return pos_profile.name
