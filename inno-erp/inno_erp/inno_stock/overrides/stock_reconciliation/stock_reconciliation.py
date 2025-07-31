import frappe
from erpnext.stock.doctype.inventory_dimension.inventory_dimension import (
	get_inventory_dimensions,
)
from erpnext.stock.doctype.stock_reconciliation.stock_reconciliation import (
	StockReconciliation,
	get_stock_balance_for,
)
from frappe import _


class EmptyStockReconciliationItemsError(frappe.ValidationError):
	pass


class InnoStockReconciliation(StockReconciliation):
	def remove_items_with_no_change(self):
		"""Remove items if qty or rate is not changed"""
		self.difference_amount = 0.0

		def _changed(item):
			if item.current_serial_and_batch_bundle:
				bundle_data = frappe.get_all(
					"Serial and Batch Bundle",
					filters={"name": item.current_serial_and_batch_bundle},
					fields=["total_qty as qty", "avg_rate as rate"],
				)[0]

				bundle_data.qty = abs(bundle_data.qty)
				self.calculate_difference_amount(item, bundle_data)

				return True

			inventory_dimensions_dict = {}
			if not item.batch_no and not item.serial_no:
				for dimension in get_inventory_dimensions():
					if item.get(dimension.get("fieldname")):
						inventory_dimensions_dict[dimension.get("fieldname")] = item.get(
							dimension.get("fieldname")
						)

			item_dict = get_stock_balance_for(
				item.item_code,
				item.warehouse,
				self.posting_date,
				self.posting_time,
				batch_no=item.batch_no,
				inventory_dimensions_dict=inventory_dimensions_dict,
				row=item,
				company=self.company,
			)

			# set default as current rates
			if item.qty is None:
				item.qty = item_dict.get("qty")

			if item.valuation_rate is None:
				item.valuation_rate = item_dict.get("rate")

			if item_dict.get("serial_nos"):
				item.current_serial_no = item_dict.get("serial_nos")
				if self.purpose == "Stock Reconciliation" and not item.serial_no and item.qty:
					item.serial_no = item.current_serial_no

			item.current_qty = item_dict.get("qty")
			item.current_valuation_rate = item_dict.get("rate")
			self.calculate_difference_amount(item, item_dict)
			return True

		items = list(filter(lambda d: _changed(d), self.items))

		if not items:
			frappe.throw(
				_("None of the items have any change in quantity or value."),
				EmptyStockReconciliationItemsError,
			)

		elif len(items) != len(self.items):
			self.items = items
			for i, item in enumerate(self.items):
				item.idx = i + 1
			frappe.msgprint(_("Removed items with no change in quantity or value."))


@frappe.whitelist()
def get_history_of_items(item_codes, warehouse=None):
	item_codes = frappe.parse_json(item_codes)
	if not item_codes:
		return {
			"orders": [],
			"purchases": [],
		}

	orders = get_history_of_sales_orders(item_codes, warehouse) + get_history_of_sales_invoices(
		item_codes, warehouse
	)

	return {
		"orders": orders,
		"purchases": get_history_of_purchase_transactions(item_codes, warehouse),
	}


def get_history_of_sales_orders(item_codes, warehouse=None):
	SalesOrder = frappe.qb.DocType("Sales Order")
	SalesOrderItem = frappe.qb.DocType("Sales Order Item")

	orders = (
		frappe.qb.from_(SalesOrderItem)
		.inner_join(SalesOrder)
		.on(SalesOrder.name == SalesOrderItem.parent)
		.where(SalesOrderItem.item_code.isin(item_codes))
		.select(
			SalesOrderItem.parent.as_("order"),
			SalesOrderItem.item_code,
			SalesOrderItem.qty,
			SalesOrderItem.delivery_date,
			SalesOrderItem.creation,
		)
		.orderby(SalesOrderItem.delivery_date, order=frappe.qb.desc)
	)

	if warehouse:
		orders = orders.where(SalesOrder.set_warehouse == warehouse)

	orders = orders.run(as_dict=True)

	return list(
		map(
			lambda order: order.update({"reference_type": "Sales Order"}),
			orders,
		)
	)


def get_history_of_sales_invoices(item_codes, warehouse=None):
	SalesInvoice = frappe.qb.DocType("Sales Invoice")
	SalesInvoiceItem = frappe.qb.DocType("Sales Invoice Item")
	invoices = (
		frappe.qb.from_(SalesInvoiceItem)
		.inner_join(SalesInvoice)
		.on(SalesInvoice.name == SalesInvoiceItem.parent)
		.where((SalesInvoiceItem.item_code.isin(item_codes)) & (SalesInvoiceItem.sales_order.isnull()))
		.select(
			SalesInvoiceItem.parent.as_("order"),
			SalesInvoiceItem.item_code,
			SalesInvoiceItem.qty,
			SalesInvoiceItem.creation,
		)
		.orderby(SalesInvoiceItem.creation, order=frappe.qb.desc)
	)

	if warehouse:
		invoices = invoices.where(SalesInvoice.set_warehouse == warehouse)

	invoices = invoices.run(as_dict=True)

	return list(
		map(
			lambda invoice: invoice.update({"reference_type": "Sales Invoice"}),
			invoices,
		)
	)


def get_history_of_purchase_transactions(item_codes, warehouse=None):
	PurchaseInvoice = frappe.qb.DocType("Purchase Invoice")
	PurchaseInvoiceItem = frappe.qb.DocType("Purchase Invoice Item")

	PurchaseReceiptItem = frappe.qb.DocType("Purchase Receipt Item")

	purchase_orders = (
		frappe.qb.from_(PurchaseInvoiceItem)
		.inner_join(PurchaseInvoice)
		.on(PurchaseInvoice.name == PurchaseInvoiceItem.parent)
		.left_join(PurchaseReceiptItem)
		.on(
			(PurchaseReceiptItem.purchase_invoice == PurchaseInvoiceItem.parent)
			& (PurchaseReceiptItem.item_code == PurchaseInvoiceItem.item_code)
		)
		.where(
			(PurchaseInvoice.docstatus == 1)
			& (PurchaseReceiptItem.name.isnull())
			& (PurchaseInvoiceItem.item_code.isin(item_codes))
		)
		.select(
			PurchaseInvoiceItem.parent.as_("purchase"),
			PurchaseInvoiceItem.item_code,
			PurchaseInvoiceItem.qty,
			PurchaseInvoice.due_date,
		)
		.orderby(PurchaseInvoice.due_date, order=frappe.qb.desc)
	)

	if warehouse:
		purchase_orders = purchase_orders.where(PurchaseInvoice.set_warehouse == warehouse)

	return purchase_orders.run(as_dict=True)
