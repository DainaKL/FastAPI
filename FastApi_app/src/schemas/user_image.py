from src.schemas.base import BaseSchema


class UserImage(BaseSchema):
    id: int
    url: str

    class Config:
        from_attributes = True
