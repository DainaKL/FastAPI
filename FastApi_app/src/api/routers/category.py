from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import get_category_use_cases
from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.schemas.category import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    return await use_cases.get_all(skip=skip, limit=limit)


@router.get("/{id}", response_model=Category)
async def get_category(
    id: int,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    try:
        return await use_cases.get_by_id(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    try:
        return await use_cases.get_by_slug(slug)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    return await use_cases.create(category_data)


@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    try:
        return await use_cases.update(id, category_data)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")


@router.delete("/{id}")
async def delete_category(
    id: int,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    try:
        await use_cases.delete(id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Category not found")
