from typing import List

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException, DatabaseOperationException)
from src.infrastructure.sqlite.models.category import Category as CategoryModel


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CategoryModel]:
        try:
            stmt = select(CategoryModel).offset(skip).limit(limit)
            return list(self.session.execute(stmt).scalars().all())
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_all", str(e))

    def get_by_id(self, category_id: int) -> CategoryModel:
        try:
            stmt = select(CategoryModel).where(CategoryModel.id == category_id)
            category = self.session.execute(stmt).scalar_one_or_none()
            if not category:
                raise CategoryNotFoundException(category_id=category_id)
            return category
        except CategoryNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_id", str(e))

    def get_by_slug(self, slug: str) -> CategoryModel:
        try:
            stmt = select(CategoryModel).where(CategoryModel.slug == slug)
            category = self.session.execute(stmt).scalar_one_or_none()
            if not category:
                raise CategoryNotFoundException(slug=slug)
            return category
        except CategoryNotFoundException:
            raise
        except SQLAlchemyError as e:
            raise DatabaseOperationException("get_by_slug", str(e))

    def create(self, **kwargs) -> CategoryModel:
        try:
            category = CategoryModel(**kwargs)
            self.session.add(category)
            self.session.flush()
            self.session.refresh(category)
            return category
        except IntegrityError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("create", str(e))

    def update(self, category_id: int, **kwargs) -> CategoryModel:
        try:
            category = self.get_by_id(category_id)
            for key, value in kwargs.items():
                if hasattr(category, key):
                    setattr(category, key, value)
            self.session.flush()
            self.session.refresh(category)
            return category
        except CategoryNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("update", str(e))

    def delete(self, category_id: int) -> None:
        try:
            category = self.get_by_id(category_id)
            self.session.delete(category)
            self.session.flush()
        except CategoryNotFoundException:
            raise
        except SQLAlchemyError as e:
            self.session.rollback()
            raise DatabaseOperationException("delete", str(e))
