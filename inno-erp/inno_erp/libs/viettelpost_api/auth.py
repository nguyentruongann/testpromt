from .typing import LoginRequest, LoginResponse


class ViettelPostAuthApi:
	def __init__(self, client):
		self.client = client

	def login(self, username: str, password: str):
		"""Login to ViettelPost and get access token"""
		login_request = LoginRequest(username=username, password=password)

		payload = {"USERNAME": login_request.username, "PASSWORD": login_request.password}

		response = self.client.make_request(url="/v2/user/Login", method="POST", json=payload)

		# Update client with new token
		data = response.get("data", {})
		if "token" in data:
			self.client.access_token = data["token"]

		return LoginResponse(**response)

	def validate_token(self):
		"""Validate current token by making a simple API call"""
		try:
			response = self.client.make_request(url="/v2/user/listInventory", method="GET")
			return {"valid": True, "message": "Token is valid"}
		except Exception as e:
			return {"valid": False, "message": str(e)}

	def refresh_token(self, username: str, password: str):
		"""Refresh token by re-logging in"""
		return self.login(username, password)
