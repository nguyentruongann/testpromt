import frappe
from frappe.utils import update_progress_bar
from redis.commands.json.path import Path
from redis.commands.search.field import TextField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from redis.exceptions import ResponseError


class RedisFullTextSearch:
	def __init__(self, index_name, shared=False):
		self.r = frappe.cache()
		self.index = self.r.ft(f"idx:{index_name}")
		self.index_name = index_name
		self.shared = shared

	def get_schema(self):
		return (
			TextField("$.name", as_name="name"),
			TextField("$.content", as_name="content"),
		)

	# def get_fields_to_search(self):
	# 	return ["name", "content"]

	def get_id(self):
		return "name"

	def get_items_to_index(self):
		"""Get all documents to be indexed conforming to the schema"""
		return []

	def get_document_to_index(self, doc_name):
		return {}

	def build(self):
		"""Build search index for all documents"""
		self.documents = self.get_items_to_index()
		self.build_index()

	def update_index_by_name(self, doc_name):
		document = self.get_document_to_index(doc_name)
		if document:
			self.update_index(document)

	def remove_document_from_index(self, doc_name):
		if not doc_name:
			return

		self.r.json().delete(f"{self.get_prefix()}:{doc_name}")

	def update_index(self, document):
		self.r.json().set(f"{self.get_prefix()}:{document[self.get_id()]}", Path.root_path(), document)

	def create_index(self, force_del=False):
		if self.exist_index():
			if force_del:
				self.drop_index()
			return

		self.index.create_index(
			self.get_schema(),
			definition=IndexDefinition(
				prefix=[self.get_prefix()],
				index_type=IndexType.JSON,
			),
		)

	def build_index(self):
		self.create_index()
		for i, document in enumerate(self.documents):
			self.r.json().set(f"{self.get_prefix()}:{document[self.get_id()]}", Path.root_path(), document)
			update_progress_bar("Building Index", i, len(self.documents))

	def parse_result(self, result):
		return frappe.parse_json(result)

	def search(self, query):
		result = self.index.search(query)
		return [self.parse_result(r.json) for r in result.docs], result.total

	def exist_index(self) -> bool:
		try:
			self.index.info()

			return True
		except ResponseError:
			return False

	def drop_index(self):
		self.index.dropindex()

	def get_prefix(self):
		return f"{frappe.conf.db_name}|{self.index_name}" if not self.shared else f"{self.index_name}"

	@staticmethod
	def escape_query(query_str):
		return query_str.strip().replace("-", " ").replace("%", " ")
