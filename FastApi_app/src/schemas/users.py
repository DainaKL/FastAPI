from pydantic import SecretStr
from src.schemas.base import BaseSchema

class User(BaseSchema):
    login: str
    password: SecretStr