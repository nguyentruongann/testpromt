__all__ = ["BaseApi"]


class BaseApi:
	DOMAIN_APIS: dict = {}  # noqa: RUF012

	def __getattr__(self, attr):
		if attr not in self.__dict__:
			self.__setattr__(attr, self.DOMAIN_APIS[attr](self.client))
		return self.__dict__[attr]
