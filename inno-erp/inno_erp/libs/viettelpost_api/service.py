from .typing import ServiceRequest, ServiceResponse


class ViettelPostServiceApi:
	def __init__(self, client):
		self.client = client

	def list_services(self, service_type: int = 2):
		"""Get list of available services"""
		service_request = ServiceRequest(service_type=service_type)

		payload = {"TYPE": service_request.service_type}

		response = self.client.make_request(url="/v2/categories/listService", method="POST", json=payload)
		return ServiceResponse(**response)

	def list_extra_services(self):
		"""Get list of available extra services"""
		response = self.client.make_request(url="/v2/categories/listServiceExtra", method="GET")
		return ServiceResponse(**response)
