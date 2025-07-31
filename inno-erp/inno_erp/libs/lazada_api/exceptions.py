class LazadaException(Exception):
	"""Custom exception for Lazada API errors."""

	def __init__(
		self,
		success: bool = False,
		message: str = "An error occurred",
		error_code: str = "",
		request_id: str = "",
		error: dict | None = None,
		http_status_code: int | None = None,
	):
		self.success = success
		self.message = message
		self.error_code = error_code
		self.request_id = request_id
		self.error = error or {}
		self.http_status_code = http_status_code

		# Create a comprehensive error message
		error_msg = f"Lazada API Error: {message}"
		if error_code:
			error_msg += f" (Code: {error_code})"
		if request_id:
			error_msg += f" (Request ID: {request_id})"
		if http_status_code:
			error_msg += f" (HTTP: {http_status_code})"

		super().__init__(error_msg)

	def __str__(self):
		return f"LazadaException(success={self.success}, message='{self.message}', error_code='{self.error_code}')"

	def __repr__(self):
		return self.__str__()
