from fastapi import HTTPException, status
from typing import List
from src.infrastructure.sqlite.database import database
from src.infrastructure.sqlite.repositories.category_repository import (
    CategoryRepository,
)
from src.infrastructure.sqlite.models.category import Category as CategoryModel
from src.schemas.category import CategoryCreate, CategoryUpdate, Category


class CategoryUseCases:
    def __init__(self):
        self._database = database

    async def create(self, data: CategoryCreate) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            category = CategoryModel(**data.model_dump())
            created = repo.create(category)
            return Category.model_validate(created, from_attributes=True)

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Category]:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            categories = repo.get_all(skip=skip, limit=limit)
            return [
                Category.model_validate(c, from_attributes=True) for c in categories
            ]

    async def get_by_id(self, category_id: int) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return Category.model_validate(category, from_attributes=True)

    async def get_by_slug(self, slug: str) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_slug(slug)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            return Category.model_validate(category, from_attributes=True)

    async def update(self, category_id: int, data: CategoryUpdate) -> Category:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            update_dict = {k: v for k, v in data.model_dump().items() if v is not None}
            updated = repo.update(category, update_dict)
            return Category.model_validate(updated, from_attributes=True)

    async def delete(self, category_id: int) -> None:
        with self._database.session() as session:
            repo = CategoryRepository(session)
            category = repo.get_by_id(category_id)
            if not category:
                raise HTTPException(status_code=404, detail="Category not found")
            repo.delete(category)
