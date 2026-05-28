from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dependencies.auth import get_current_user
from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.schemas.users import User
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    ConflictException,
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
    db: AsyncSession = Depends(get_db),
):
    from src.domain.category.use_cases.get_categories import GetCategoriesUseCase

    use_case = GetCategoriesUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Category)
async def get_category(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    validate_id(id)
    from src.domain.category.use_cases.get_category import GetCategoryUseCase

    use_case = GetCategoryUseCase()
    return await use_case.execute(db, id)


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    from src.domain.category.use_cases.get_category_by_slug import (
        GetCategoryBySlugUseCase,
    )

    use_case = GetCategoryBySlugUseCase()
    return await use_case.execute(db, slug)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    from src.domain.category.use_cases.create_category import CreateCategoryUseCase

    use_case = CreateCategoryUseCase()
    try:
        result = await use_case.execute(db, category_data, current_user.id)
        await db.commit()
        return result
    except Exception as e:
        if "already exists" in str(e):
            raise ConflictException(detail=str(e))
        raise


@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    from src.domain.category.use_cases.update_category import UpdateCategoryUseCase

    use_case = UpdateCategoryUseCase()
    try:
        result = await use_case.execute(
            db, id, category_data, current_user.id, current_user.is_admin
        )
        await db.commit()
        return result
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.delete("/{id}")
async def delete_category(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    validate_id(id)
    from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase

    use_case = DeleteCategoryUseCase()
    try:
        await use_case.execute(db, id, current_user.id, current_user.is_admin)
        await db.commit()
        return {"status": "success", "message": f"Category {id} deleted"}
    except Exception as e:
        raise NotFoundException(detail=str(e))
