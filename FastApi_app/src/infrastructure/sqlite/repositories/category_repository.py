from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.models import Category
from src.infrastructure.sqlite.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: Session):
        super().__init__(session, Category)
    
    def get_by_slug(self, slug: str) -> Optional[Category]:
        stmt = select(Category).where(Category.slug == slug)
        return self.session.execute(stmt).scalar_one_or_none()
