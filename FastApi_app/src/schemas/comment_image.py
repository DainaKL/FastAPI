from src.schemas.base import BaseSchema


class CommentImage(BaseSchema):
    id: int
    url: str

    class Config:
        from_attributes = True
