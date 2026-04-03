from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.comment import Comment as CommentModel


class CommentRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, comment: CommentModel) -> CommentModel:
        self.session.add(comment)
        self.session.flush()
        return comment

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        return self.session.query(CommentModel).offset(skip).limit(limit).all()

    def get_published(self, skip: int = 0, limit: int = 100) -> List[CommentModel]:
        return (
            self.session.query(CommentModel)
            .filter(CommentModel.is_published == True)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_id(self, comment_id: int) -> Optional[CommentModel]:
        return (
            self.session.query(CommentModel)
            .filter(CommentModel.id == comment_id)
            .first()
        )

    def get_by_post(
        self, post_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        return (
            self.session.query(CommentModel)
            .filter(CommentModel.post_id == post_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_by_author(
        self, author_id: int, skip: int = 0, limit: int = 100
    ) -> List[CommentModel]:
        return (
            self.session.query(CommentModel)
            .filter(CommentModel.author_id == author_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def update(self, comment: CommentModel, data: dict) -> CommentModel:
        for key, value in data.items():
            setattr(comment, key, value)
        self.session.flush()
        return comment

    def delete(self, comment: CommentModel) -> None:
        self.session.delete(comment)
        self.session.flush()
