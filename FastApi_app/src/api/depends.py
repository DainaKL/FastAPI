from fastapi import Depends

from src.infrastructure.sqlite.database import get_db
from src.infrastructure.sqlite.repositories.user_repository import UserRepository
from src.infrastructure.sqlite.repositories.post_repository import PostRepository
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository
from src.infrastructure.sqlite.repositories.location_repository import LocationRepository
from src.infrastructure.sqlite.repositories.comment_repository import CommentRepository

from sqlalchemy.orm import Session


# Зависимости для репозиториев
def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
    return UserRepository(db)

def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostRepository(db)

def get_category_repository(db: Session = Depends(get_db)) -> CategoryRepository:
    return CategoryRepository(db)

def get_location_repository(db: Session = Depends(get_db)) -> LocationRepository:
    return LocationRepository(db)

def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    return CommentRepository(db)
