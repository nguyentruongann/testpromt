import frappe
from erpnext.stock.doctype.stock_entry.stock_entry import make_stock_in_entry as erpnext_make_stock_in_entry
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt


@frappe.whitelist()
def make_stock_in_entry(source_name, target_doc=None):
	entry = frappe.db.get_value(
		"Stock Entry", source_name, ["stock_entry_type", "add_to_transit"], as_dict=True
	)
	if entry.stock_entry_type != "Material Transfer" or entry.add_to_transit is False:
		return erpnext_make_stock_in_entry(source_name, target_doc)

	def set_missing_values(source, target):
		target.stock_entry_type = "Material Transfer"
		target.set_missing_values()

		if not frappe.db.get_single_value("Stock Settings", "use_serial_batch_fields"):
			target.make_serial_and_batch_bundle_for_transfer()

	def update_item(source_doc, target_doc, source_parent):
		if source_doc.material_request_item and source_doc.material_request:
			add_to_transit = frappe.db.get_value("Stock Entry", source_name, "add_to_transit")
			if add_to_transit:
				warehouse = frappe.get_value(
					"Material Request Item", source_doc.material_request_item, "warehouse"
				)
				target_doc.t_warehouse = warehouse

		target_doc.s_warehouse = source_parent.to_warehouse
		target_doc.t_warehouse = source_parent.custom_end_warehouse
		target_doc.qty = source_doc.qty - source_doc.transferred_qty

	doclist = get_mapped_doc(
		"Stock Entry",
		source_name,
		{
			"Stock Entry": {
				"doctype": "Stock Entry",
				"field_map": {
					"name": "outgoing_stock_entry",
					"to_warehouse": "from_warehouse",
					"custom_end_warehouse": "to_warehouse",
				},
				"validation": {"docstatus": ["=", 1]},
			},
			"Stock Entry Detail": {
				"doctype": "Stock Entry Detail",
				"field_map": {
					"name": "ste_detail",
					"parent": "against_stock_entry",
					"serial_no": "serial_no",
					"batch_no": "batch_no",
				},
				"postprocess": update_item,
				"condition": lambda doc: flt(doc.qty) - flt(doc.transferred_qty) > 0.00001,
			},
		},
		target_doc,
		set_missing_values,
	)

	return doclist
