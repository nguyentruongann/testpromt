from abc import ABC, abstractmethod


class BaseConnector(ABC):
	@abstractmethod
	def get_products(self, filters: dict):
		pass

	@abstractmethod
	def get_orders(self, filters: dict):
		pass

	@abstractmethod
	def create_product(self, filters: dict):
		pass

	@abstractmethod
	def update_product(self, filters: dict):
		pass

	@abstractmethod
	def update_stock(self, filters: dict):
		pass

	@abstractmethod
	def update_price(self, filters: dict):
		pass

	@abstractmethod
	def update_quantity(self, filters: dict):
		pass
