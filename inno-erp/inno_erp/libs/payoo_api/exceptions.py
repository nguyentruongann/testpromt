class PayooException(Exception):
	"""Lớp exception cơ sở cho các lỗi của SDK."""

	def __init__(self, message):
		super().__init__(message)


class PayooAPIException(PayooException):
	"""Ném ra khi API trả về lỗi."""

	def __init__(self, message, return_code=None):
		super().__init__(message)
		self.return_code = return_code

	def __str__(self):
		if self.return_code is not None:
			return f"[ReturnCode: {self.return_code}] {self.args[0]}"
		return self.args[0]


class SignatureVerificationError(PayooException):
	"""Ném ra khi xác thực chữ ký thất bại."""

	pass
