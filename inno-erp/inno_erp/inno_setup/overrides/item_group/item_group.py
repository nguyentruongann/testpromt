from erpnext.setup.doctype.item_group.item_group import ItemGroup
from frappe.utils import get_abbr

from inno_erp.utils.string import scrub


class InnoItemGroup(ItemGroup):
	def validate(self):
		super().validate()
		if not self.custom_abbr:
			self.custom_abbr = get_abbr(self.name, 3) if " " in self.name else self.name

		self.custom_abbr = scrub(self.custom_abbr, separator="-")
