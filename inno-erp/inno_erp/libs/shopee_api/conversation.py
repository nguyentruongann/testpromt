from .client import ShopeeClient

CONVERSATION_API_PATH = "/api/v2/sellerchat"


class ConversationAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_conversation_list(
		self,
		direction="older",
		type="all",
		page_size=10,
		next_timestamp_nano="9999999999999999999",
		conversation_id="",
	):
		return self.client.make_request(
			"GET",
			f"{CONVERSATION_API_PATH}/get_conversation_list",
			params={
				"direction": direction,
				"type": type,
				"page_size": page_size,
				"next_timestamp_nano": next_timestamp_nano,
				"conversation_id": conversation_id,
			},
		)
