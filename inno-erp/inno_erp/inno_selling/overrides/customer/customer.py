import frappe
from erpnext.selling.doctype.customer import customer
from erpnext.selling.doctype.customer.customer import Customer


class InnoCustomer(Customer):
	def create_primary_address(self):
		from frappe.contacts.doctype.address.address import get_address_display

		if self.flags.is_new_doc and self.get("address_line1"):
			address = inno_make_address(self)
			address_display = get_address_display(address.name)

			self.db_set("customer_primary_address", address.name)
			self.db_set("primary_address", address_display)


def inno_make_address(args, is_primary_address=1, is_shipping_address=1):
	party_name_key = "customer_name" if args.doctype == "Customer" else "supplier_name"
	default_country = frappe.get_value("System Settings", None, "country")

	address = frappe.get_doc(
		{
			"doctype": "Address",
			"address_title": args.get(party_name_key),
			"address_line1": args.get("address_line1"),
			"address_line2": args.get("address_line2"),
			"address_type": args.get("address_type"),
			"city": args.get("custom_address_location") or "U/A",
			"custom_ward": args.get("custom_ward"),
			"custom_address_location": args.get("custom_address_location"),
			"state": args.get("state"),
			"pincode": args.get("pincode"),
			"country": args.get("country") or default_country,
			"is_primary_address": is_primary_address,
			"is_shipping_address": is_shipping_address,
			"links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
		}
	)

	if flags := args.get("flags"):
		address.insert(ignore_permissions=flags.get("ignore_permissions"))
	else:
		address.insert()

	return address


customer.make_address = inno_make_address
