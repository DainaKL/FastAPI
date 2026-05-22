from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.api.depends import get_category_use_cases
from src.dependencies.auth import get_current_user
from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    ConflictException,
    CategoryForbiddenException,
    InvalidIDException,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=list[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_all(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Category)
async def get_category(
    id: int,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    try:
        return await use_cases.get_by_id(db, id)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await use_cases.get_by_slug(db, slug)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await use_cases.create(db, category_data)
    except Exception as e:
        if "already exists" in str(e):
            raise ConflictException(detail=str(e))
        raise


@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    if not current_user.get("is_admin"):
        raise CategoryForbiddenException(action="редактировать")
    try:
        return await use_cases.update(db, id, category_data)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.delete("/{id}")
async def delete_category(
    id: int,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    if not current_user.get("is_admin"):
        raise CategoryForbiddenException(action="удалять")
    try:
        await use_cases.delete(db, id)
        return {"status": "success", "message": f"Category {id} deleted"}
    except Exception as e:
        raise NotFoundException(detail=str(e))
