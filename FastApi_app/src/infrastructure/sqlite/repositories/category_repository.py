from typing import List, Optional
from sqlalchemy.orm import Session
from src.infrastructure.sqlite.models.category import Category as CategoryModel


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, category: CategoryModel) -> CategoryModel:
        self.session.add(category)
        self.session.flush()
        return category

    def get_all(self, skip: int = 0, limit: int = 100) -> List[CategoryModel]:
        return self.session.query(CategoryModel).offset(skip).limit(limit).all()

    def get_by_id(self, category_id: int) -> Optional[CategoryModel]:
        return (
            self.session.query(CategoryModel)
            .filter(CategoryModel.id == category_id)
            .first()
        )

    def get_by_slug(self, slug: str) -> Optional[CategoryModel]:
        return (
            self.session.query(CategoryModel).filter(CategoryModel.slug == slug).first()
        )

    def update(self, category: CategoryModel, data: dict) -> CategoryModel:
        for key, value in data.items():
            setattr(category, key, value)
        self.session.flush()
        return category

    def delete(self, category: CategoryModel) -> None:
        self.session.delete(category)
        self.session.flush()
