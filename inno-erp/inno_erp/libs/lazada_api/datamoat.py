from datetime import datetime, timedelta, timezone

from .client import LazadaClient
from .typing import (
	LazadaComputeRiskRequest,
	LazadaComputeRiskResponse,
	LazadaLoginRequest,
	LazadaLoginResponse,
)


class LazadaDataMoat:
	def __init__(self, client: LazadaClient):
		self.client = client

	def compute_risk(self, request: LazadaComputeRiskRequest) -> LazadaComputeRiskResponse:
		path = "/datamoat/compute_risk"
		vn_tz = timezone(timedelta(hours=7))
		current_time = int(datetime.now(vn_tz).timestamp() * 1000)

		params = {
			"time": str(current_time),
			"appName": request.app_name,
			"userId": request.user_id,
			"userIp": request.user_ip,
			"ati": request.ati,
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaComputeRiskResponse(**response)

	def login(self, request: LazadaLoginRequest) -> LazadaLoginResponse:
		path = "/datamoat/login"
		vn_tz = timezone(timedelta(hours=7))
		current_time = int(datetime.now(vn_tz).timestamp() * 1000)

		params = {
			"time": str(current_time),
			"appName": request.app_name,
			"userId": request.user_id,
			"tid": request.tid,
			"userIp": request.user_ip,
			"ati": request.ati,
			"loginResult": request.login_result,
			"loginMessage": request.login_message,
		}
		response = self.client.make_request(path, params=params, method="POST")
		return LazadaLoginResponse(**response)
