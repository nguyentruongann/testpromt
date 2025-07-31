import json

from .client import ZaloClient
from .typing import (
	ZaloListUsers,
	ZaloListUsersRequest,
	ZaloListUsersResponse,
	ZaloUserDetail,
	ZaloUserDetailResponse,
)


class UserAPI:
	def __init__(self, client: ZaloClient | None = None, access_token: str | None = None):
		if client is None:
			self.client = ZaloClient(access_token=access_token)
		else:
			self.client = client

	def get_user_detail(self, user_id) -> ZaloUserDetail:
		"""
		Get user details from Zalo Official Account.

		Args:
		    user_id (str): User ID to retrieve details for

		Returns:
		    ZaloUserDetailResponse: Response containing user details

		Raises:
		    ZaloException: If API returns an error
		"""

		data = {
			"user_id": user_id,
		}

		return self.client.make_request(
			"/v3.0/oa/user/detail",
			"GET",
			params={"data": json.dumps(data)},
			typing=ZaloUserDetailResponse,
		).data

	def list_users(self, data: ZaloListUsersRequest) -> ZaloListUsers:
		"""
		List users from Zalo Official Account.

		Args:
		    data (ZaloListUsersRequest): Request containing user IDs to retrieve details for

		Returns:
		    ZaloListUsersResponse: Response containing list of users

		Raises:
		    ZaloException: If API returns an error
		"""
		return self.client.make_request(
			"/v3.0/oa/user/getlist",
			"GET",
			params={"data": data.model_dump_json(exclude_none=True)},
			typing=ZaloListUsersResponse,
		).data
