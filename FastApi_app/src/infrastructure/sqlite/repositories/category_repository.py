from typing import Type
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.category import CategoryCreate as CategorySchema
from src.core.exceptions.database_exceptions import DatabaseOperationException


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int):
        if category_id <= 0:
            return None
        query = select(self._model).where(self._model.id == category_id)
        return session.scalar(query)

    def get_by_slug(self, session: Session, slug: str):
        if not slug:
            return None
        query = select(self._model).where(self._model.slug == slug)
        return session.scalar(query)

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, category: CategorySchema) -> CategoryModel:
        try:
            query = (
                insert(self._model).values(category.model_dump()).returning(self._model)
            )
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, category_id: int, **kwargs):
        query = (
            update(self._model)
            .where(self._model.id == category_id)
            .values(**kwargs)
            .returning(self._model)
        )
        return session.scalar(query)

    def delete(self, session: Session, category_id: int):
        query = delete(self._model).where(self._model.id == category_id)
        result = session.execute(query)
        return result.rowcount > 0
