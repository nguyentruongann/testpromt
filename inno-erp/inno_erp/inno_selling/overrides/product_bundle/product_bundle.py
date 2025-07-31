import frappe
from erpnext.selling.doctype.product_bundle import product_bundle
from erpnext.selling.doctype.product_bundle.product_bundle import ProductBundle


class InnoProductBundle(ProductBundle):
	def validate(self):
		super().validate()

	def on_change(self):
		if self.new_item_code:
			frappe.db.set_value("Item", self.new_item_code, {
				"disabled": self.disabled or 0,
			})
