from pydantic import BaseModel


class ViettelPostResponse(BaseModel):
	status: int
	error: bool
	message: str


class LoginRequest(BaseModel):
	username: str
	password: str


class UserData(BaseModel):
	userId: int
	token: str
	partner: int
	phone: str | None = None
	postcode: str | None = None
	expired: int | None = None
	encrypted: str | None = None
	source: int | None = None
	infoUpdated: bool = True


class LoginResponse(ViettelPostResponse):
	data: UserData | None = None
