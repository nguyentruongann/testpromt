from .client import ZaloClient
from .typing import ZaloAttachmentElement, ZaloException, ZaloSendMessage, ZaloSendMessageResponse

MESSAGE_MAX_LENGTH = 2000


class MessageAPI:
	def __init__(self, client: ZaloClient | None = None, access_token: str | None = None):
		if client is None:
			self.client = ZaloClient(access_token=access_token)
		else:
			self.client = client

	def send_message(self, user_id, message) -> ZaloSendMessage:
		"""
		Send a message to a Zalo user.

		Args:
		    user_id (str): The ID of the user to send the message to
		    message (str): The text message to send

		Returns:
		    ZaloSendMessageResponse: Response containing message details and quota information

		Raises:
		    ZaloException: If the API request fails or returns an error
		"""

		if len(message) > MESSAGE_MAX_LENGTH:
			raise ZaloException(
				f"Message length exceeds the maximum length of {MESSAGE_MAX_LENGTH} characters"
			)

		data = {
			"recipient": {
				"user_id": user_id,
			},
			"message": {
				"text": message,
			},
		}

		return self.client.make_request(
			"/v3.0/oa/message/cs", "POST", json=data, typing=ZaloSendMessageResponse
		).data

	def send_message_with_images(
		self, user_id, message, images: list[ZaloAttachmentElement]
	) -> ZaloSendMessage:
		"""
		Send a message with attached images to a Zalo user.

		Args:
		    user_id (str): The ID of the user to send the message to
		    message (str): The text message to send
		    images (list[ZaloAttachmentElement]): List of image attachments, each containing media_type and url/attachment_id

		Returns:
		    ZaloSendMessageResponse: Response containing message details and quota information

		Raises:
		    ZaloException: If the API request fails or returns an error
		"""

		images = [image.model_dump() for image in images]
		for image in images:
			if image.get("attachment_id") is None:
				del image["attachment_id"]

			if image.get("url") is None:
				del image["url"]

		data = {
			"recipient": {
				"user_id": user_id,
			},
			"message": {
				"text": message,
				"attachment": {
					"type": "template",
					"payload": {
						"template_type": "media",
						"elements": [images[0]],
					},
				},
			},
		}

		return self.client.make_request(
			"/v3.0/oa/message/cs", "POST", json=data, typing=ZaloSendMessageResponse
		).data
