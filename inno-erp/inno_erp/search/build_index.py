import frappe
from frappe.search.full_text_search import FullTextSearch
from whoosh.fields import ID, TEXT, Schema


class ItemSearch(FullTextSearch):
	def get_schema(self):
		return Schema(
			name=ID(stored=True),
			image=TEXT(stored=True),
			item_name=TEXT(stored=True),
			item_code=TEXT(stored=True),
			description=TEXT(stored=True),
			brand=TEXT(stored=True),
			item_group=TEXT(stored=True),
		)

	def get_items_to_index(self):
		items = frappe.get_all(
			"Item",
			filters={"disabled": 0},
			fields=["name", "item_name", "item_code", "description", "brand", "item_group"],
		)

		documents = []
		for item in items:
			doc = {
				"name": item.name,
				"image": item.image or "",
				"item_name": item.item_name or "",
				"item_code": item.item_code or "",
				"description": item.description or "",
				"brand": item.brand or "",
				"item_group": item.item_group or "",
			}
			documents.append(doc)

		return documents

	def get_fields_to_search(self):
		return ["item_name", "item_code", "description", "brand", "item_group"]

	def parse_result(self, result):
		return {
			"name": result.get("name"),
			"image": result.get("image"),
			"item_name": result.get("item_name"),
			"item_code": result.get("item_code"),
			"description": result.get("description"),
			"brand": result.get("brand"),
			"item_group": result.get("item_group"),
		}


def build():
	"""Build the item search index"""
	builder = ItemSearch("item_search")
	builder.build()
