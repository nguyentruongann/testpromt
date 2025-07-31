import frappe

from inno_erp.search.item_search import ItemSearch


def on_change(doc, method):
	doctype = doc.doctype
	if method == "on_trash":
		if doctype == "Omni Item":
			frappe.enqueue(
				"inno_erp.search.ecom_index.reindex_on_trash",
				queue="default",
				job_id="ecom_index_on_trash",
				doctype=doctype,
				name=doc.name,
			)

	elif method == "on_change":
		if doctype == "Item":
			frappe.enqueue(
				"inno_erp.search.ecom_index.reindex_on_change",
				queue="default",
				job_id="ecom_index_on_update",
				doctype=doctype,
				name=doc.item_code,
			)
		if doctype == "Omni Item" and doc.linked_item:
			frappe.enqueue(
				"inno_erp.search.ecom_index.reindex_on_change",
				queue="default",
				job_id="ecom_index_on_update",
				doctype=doctype,
				name=doc.linked_item,
			)
		elif doctype in ["Stock Reservation Entry", "Stock Ledger Entry", "Item Price"]:
			frappe.enqueue(
				"inno_erp.search.ecom_index.reindex_on_change",
				queue="default",
				job_name="ecom_index_on_update",
				doctype=doctype,
				name=doc.item_code,
			)
		elif doctype in ["Pricing Rule"]:
			item_codes = collect_item_codes_from_pricing_rule(doc)
			for item_code in item_codes:
				frappe.enqueue(
					"inno_erp.search.ecom_index.reindex_on_change",
					queue="default",
					job_name="ecom_index_on_update",
					doctype=doctype,
					name=item_code,
				)


def collect_item_codes_from_pricing_rule(pricing_rule):
	if pricing_rule.apply_on == "Item Code":
		return frappe.db.get_all(
			"Pricing Rule Item Code", filters={"parent": pricing_rule.name}, pluck="item_code"
		)
	elif pricing_rule.apply_on == "Item Group":
		item_groups = frappe.db.get_all(
			"Pricing Rule Item Group",
			filters={"parent": pricing_rule.name},
			pluck="item_group",
		)
		return frappe.db.get_all(
			"Item",
			filters={"item_group": ("in", item_groups)},
			pluck="item_code",
		)
	elif pricing_rule.apply_on == "Brand":
		brands = frappe.db.get_all(
			"Pricing Rule Brand",
			filters={"parent": pricing_rule.name},
			pluck="brand",
		)
		return frappe.db.get_all(
			"Item",
			filters={"brand": ("in", brands)},
			pluck="item_code",
		)

	return []


def reindex_on_trash(doctype, name):
	omni_item_name = frappe.db.get_all("Omni Item", filters={"linked_item": name}, pluck="name")
	variant_of = frappe.db.get_value("Omni Item", omni_item_name, "variant_of")

	if variant_of:
		ItemSearch().remove_document_from_index(variant_of)
	else:
		ItemSearch().remove_document_from_index(omni_item_name)


def reindex_on_change(doctype, name):
	omni_item_name = frappe.db.get_all("Omni Item", filters={"linked_item": name}, pluck="name")
	variant_of = frappe.db.get_value("Omni Item", omni_item_name, "variant_of")
	if variant_of:
		ItemSearch().update_index_by_name(variant_of)
	else:
		ItemSearch().update_index_by_name(omni_item_name)
