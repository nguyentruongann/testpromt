from .client import ShopeeClient

MESSAGE_API_PATH = "/api/v2/sellerchat"


class MessageAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_message_list(self, page_size=10, offset=0, conversation_id=""):
		return self.client.make_request(
			"GET",
			f"{MESSAGE_API_PATH}/get_message",
			params={
				"page_size": page_size,
				"offset": offset,
				"conversation_id": conversation_id,
			},
		)

	def send_message(self, to_id, message_type, content):
		return self.client.make_request(
			"POST",
			f"{MESSAGE_API_PATH}/send_message",
			data={"to_id": to_id, "message_type": message_type, "content": content},
		)

	def upload_image(self, file):
		return self.client.make_request(
			"POST",
			f"{MESSAGE_API_PATH}/upload_image",
			files={"file": file},
		)

	def upload_video(self, file):
		return self.client.make_request(
			"POST",
			f"{MESSAGE_API_PATH}/upload_video",
			files={"file": file},
		)
