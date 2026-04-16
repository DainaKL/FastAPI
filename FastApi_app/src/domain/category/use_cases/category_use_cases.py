from typing import List

from fastapi import HTTPException

from src.core.exceptions.database_exceptions import (
    CategoryNotFoundException, DatabaseOperationException)
from src.core.exceptions.domain_exceptions import \
    CategoryNotFoundBySlugException
from src.core.exceptions.domain_exceptions import \
    CategoryNotFoundException as DomainCategoryNotFoundException
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import \
    CategoryRepository
from src.schemas.category import Category, CategoryCreate, CategoryUpdate


class CategoryUseCases:
    def __init__(self):
        self._database = database

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                categories = repo.get_all(skip=skip, limit=limit)
                return [
                    Category.model_validate(c, from_attributes=True) for c in categories
                ]
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_id(self, category_id: int) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                category = repo.get_by_id(category_id)
                return Category.model_validate(category, from_attributes=True)
            except CategoryNotFoundException:
                raise DomainCategoryNotFoundException(category_id=category_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def get_by_slug(self, slug: str) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                category = repo.get_by_slug(slug)
                return Category.model_validate(category, from_attributes=True)
            except CategoryNotFoundException:
                raise CategoryNotFoundBySlugException(slug=slug)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def create(self, data: CategoryCreate) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                category_dict = data.model_dump()
                category = repo.create(**category_dict)
                return Category.model_validate(category, from_attributes=True)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def update(self, category_id: int, data: CategoryUpdate) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                update_dict = {
                    k: v for k, v in data.model_dump().items() if v is not None
                }
                category = repo.update(category_id, **update_dict)
                return Category.model_validate(category, from_attributes=True)
            except CategoryNotFoundException:
                raise DomainCategoryNotFoundException(category_id=category_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())

    async def delete(self, category_id: int) -> None:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            try:
                repo.delete(category_id)
            except CategoryNotFoundException:
                raise DomainCategoryNotFoundException(category_id=category_id)
            except DatabaseOperationException as e:
                raise HTTPException(status_code=500, detail=e.get_detail())
