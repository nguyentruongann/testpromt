from pydantic import BaseModel

from .base import LazadaResponse


# Risk computation models
class LazadaComputeRiskData(BaseModel):
	riskScore: float | None = None
	riskLevel: str | None = None
	details: dict[str, any] | None = None


class LazadaComputeRiskRequest(BaseModel):
	user_id: str
	user_ip: str
	ati: str
	app_name: str = "yourAppName"


class LazadaComputeRiskResponse(LazadaResponse):
	data: LazadaComputeRiskData | None = None


# Login tracking models
class LazadaLoginData(BaseModel):
	authStatus: str | None = None
	sessionId: str | None = None
	message: str | None = None


class LazadaLoginRequest(BaseModel):
	user_id: str
	tid: str
	user_ip: str
	ati: str
	login_result: str
	login_message: str
	app_name: str = "yourAppName"


class LazadaLoginResponse(LazadaResponse):
	data: LazadaLoginData | None = None
