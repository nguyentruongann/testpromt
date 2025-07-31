from .client import ZaloClient
from .typing import ZaloException, ZaloResponse

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
SUPPORTED_EXTENSIONS = ["pdf", "doc", "docx"]


class UploadAPI:
	def __init__(self, client: ZaloClient):
		self.client = client

	def upload_file(self, file_path: str) -> ZaloResponse:
		file_extension = file_path.lower().split(".")[-1]
		if file_extension not in SUPPORTED_EXTENSIONS:
			raise ValueError(
				f"Unsupported file type. Only {', '.join(SUPPORTED_EXTENSIONS)} files are allowed."
			)

		try:
			with open(file_path, "rb") as f:
				file_binary = f.read()
				file_name = file_path.split("/")[-1]

			if len(file_binary) > MAX_FILE_SIZE:
				raise ZaloException(
					f"File size exceeds maximum allowed size of {MAX_FILE_SIZE} bytes",
					400,
				)

			return self.client.upload("file", file_name, file_binary)

		except FileNotFoundError:
			raise ZaloException(f"File not found: {file_path}", 404)
		except Exception as e:
			raise ZaloException(f"Error uploading file: {e!s}", 500)
