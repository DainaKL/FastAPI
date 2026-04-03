from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.post import Post as PostModel


class PostRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, post: PostModel) -> PostModel:
        self.session.add(post)
        self.session.flush()
        return post

    def get_all(self, skip: int = 0, limit: int = 100) -> List[PostModel]:
        return self.session.query(PostModel).offset(skip).limit(limit).all()

    def get_by_id(self, post_id: int) -> Optional[PostModel]:
        return self.session.query(PostModel).filter(PostModel.id == post_id).first()

    def update(self, post: PostModel, data: dict) -> PostModel:
        for key, value in data.items():
            setattr(post, key, value)
        self.session.flush()
        return post

    def delete(self, post: PostModel) -> None:
        self.session.delete(post)
        self.session.flush()
