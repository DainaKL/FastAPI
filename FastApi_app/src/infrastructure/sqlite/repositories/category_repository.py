from typing import Type

from sqlalchemy import insert, select, update, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.category import CategoryCreate as CategorySchema
from src.core.exceptions.database_exceptions import CategoryNotFoundException, DatabaseOperationException


class CategoryRepository:
    def __init__(self):
        self._model: Type[CategoryModel] = CategoryModel

    def get_by_id(self, session: Session, category_id: int) -> CategoryModel:
        if category_id <= 0:
            raise CategoryNotFoundException(category_id=category_id)
        query = select(self._model).where(self._model.id == category_id)
        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)
        return category

    def get_by_slug(self, session: Session, slug: str) -> CategoryModel:
        if not slug:
            raise CategoryNotFoundException(slug=slug)
        query = select(self._model).where(self._model.slug == slug)
        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException(slug=slug)
        return category

    def get_all(self, session: Session, skip: int = 0, limit: int = 100):
        query = select(self._model).offset(skip).limit(limit)
        return list(session.scalars(query).all())

    def create(self, session: Session, category: CategorySchema) -> CategoryModel:
        query = insert(self._model).values(category.model_dump()).returning(self._model)
        try:
            return session.scalar(query)
        except IntegrityError as e:
            raise DatabaseOperationException("create", str(e))

    def update(self, session: Session, category_id: int, **kwargs) -> CategoryModel:
        query = update(self._model).where(self._model.id == category_id).values(**kwargs).returning(self._model)
        category = session.scalar(query)
        if not category:
            raise CategoryNotFoundException(category_id=category_id)
        return category

    def delete(self, session: Session, category_id: int) -> None:
        query = delete(self._model).where(self._model.id == category_id)
        result = session.execute(query)
        if result.rowcount == 0:
            raise CategoryNotFoundException(category_id=category_id)
