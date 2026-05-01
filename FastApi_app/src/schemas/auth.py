from src.schemas.base import BaseSchema


class LoginRequest(BaseSchema):
    login: str
    password: str


class LoginResponse(BaseSchema):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    login: str
