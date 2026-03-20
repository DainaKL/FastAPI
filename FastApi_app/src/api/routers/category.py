from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_category_repository
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.infrastructure.sqlite.repositories.category_repository import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Получение списка всех категорий"""
    try:
        categories = repo.get_all(skip=skip, limit=limit)
        return categories
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=Category)
async def get_category(
    id: int,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Получение категории по ID"""
    category = repo.get_by_id(id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Получение категории по slug"""
    category = repo.get_by_slug(slug)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Создание новой категории"""
    try:
        category_dict = category_data.model_dump()
        new_category = repo.create(**category_dict)
        return new_category
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Обновление категории"""
    update_dict = {k: v for k, v in category_data.model_dump().items() if v is not None}
    updated = repo.update(id, **update_dict)
    if not updated:
        raise HTTPException(status_code=404, detail="Category not found")
    return updated

@router.delete("/{id}")
async def delete_category(
    id: int,
    repo: CategoryRepository = Depends(get_category_repository)
):
    """Удаление категории"""
    deleted = repo.delete(id)
    try:
        if not deleted:
            raise HTTPException(status_code=404, detail="Category not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
