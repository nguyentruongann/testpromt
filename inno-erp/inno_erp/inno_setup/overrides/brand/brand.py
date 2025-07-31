from erpnext.setup.doctype.brand.brand import Brand
from frappe.utils import get_abbr

from inno_erp.utils.string import scrub


class InnoBrand(Brand):
	def validate(self):
		if not self.custom_abbr:
			self.custom_abbr = get_abbr(self.name, 3) if " " in self.name else self.name

		self.custom_abbr = scrub(self.custom_abbr, separator="-")
