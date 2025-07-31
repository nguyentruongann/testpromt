from pydantic import BaseModel

from .auth import ViettelPostResponse


class ServiceRequest(BaseModel):
	service_type: int = 2


class ServiceItem(BaseModel):
	service_code: str
	service_name: str
	description: str | None = None


class ServiceResponse(ViettelPostResponse):
	data: list[ServiceItem] | None = None


# @dataclass
# class ExtraService:
# 	"""Extra service data structure"""

# 	service_code: str
# 	service_name: str
# 	description: str | None = None


# @dataclass
# class ServiceCategory:
# 	"""Service category data structure"""

# 	category_name: str
# 	services: list
# 	description: str | None = None
