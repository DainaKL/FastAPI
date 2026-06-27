from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dependencies.auth import get_current_user, get_current_admin_user
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.schemas.users import User
from src.domain.category.use_cases.get_categories import GetCategoriesUseCase
from src.domain.category.use_cases.get_category import GetCategoryUseCase
from src.domain.category.use_cases.get_category_by_slug import GetCategoryBySlugUseCase
from src.domain.category.use_cases.create_category import CreateCategoryUseCase
from src.domain.category.use_cases.update_category import UpdateCategoryUseCase
from src.domain.category.use_cases.delete_category import DeleteCategoryUseCase

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[Category])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetCategoriesUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/{id}", response_model=Category)
async def get_category(
    id: int,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetCategoryUseCase()
    return await use_case.execute(db, id)


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetCategoryBySlugUseCase()
    return await use_case.execute(db, slug)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = CreateCategoryUseCase()
    result = await use_case.execute(db, category_data, current_user.id)
    await db.commit()
    return result


@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = UpdateCategoryUseCase()
    result = await use_case.execute(
        db, id, category_data, current_user.id, current_user.is_admin
    )
    await db.commit()
    return result


@router.delete("/{id}")
async def delete_category(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteCategoryUseCase()
    await use_case.execute(db, id, current_user.id, current_user.is_admin)
    await db.commit()
    return {"status": "success", "message": f"Category {id} deleted"}
