from src.schemas.base import BaseSchema


class PostImage(BaseSchema):
    id: int
    url: str

    class Config:
        from_attributes = True
