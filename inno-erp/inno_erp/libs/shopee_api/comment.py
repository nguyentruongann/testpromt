from .client import ShopeeClient

COMMENT_API_PATH = "/api/v2/product"


class CommentAPI:
	def __init__(self, client: ShopeeClient):
		self.client = client

	def get_comments(self, item_id, cursor, page_size=10):
		params = {
			"item_id": item_id,
			"cursor": cursor,
			"page_size": page_size,
		}
		return self.client.make_request("GET", f"{COMMENT_API_PATH}/get_comment", params=params)

	def reply_comment(self, comment_id, reply_text):
		data = {
			"comment_list": [
				{
					"comment_id": comment_id,
					"comment": reply_text,
				}
			]
		}
		return self.client.make_request("POST", f"{COMMENT_API_PATH}/reply_comment", data=data)
