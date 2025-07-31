class ViettelPostException(Exception):
	success: bool
	message: str
	error_code: str
	log_id: str
	error: dict | None = None

	def __init__(
		self,
		success: bool = False,
		message: str = "",
		error_code: str = "",
		log_id: str = "",
		error: dict | None = None,
	):
		self.success = success
		self.message = message
		self.error_code = error_code
		self.log_id = log_id
		self.error = error
		super().__init__(message)
