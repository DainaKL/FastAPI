from fastapi import APIRouter, Depends, status

from src.api.depends import get_category_use_cases
from src.dependencies.auth import get_current_user
from src.domain.category.use_cases.category_use_cases import CategoryUseCases
from src.schemas.category import Category, CategoryCreate, CategoryUpdate
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    ConflictException,
    ForbiddenException,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundException,
    CategoryNotFoundBySlugException,
    CategorySlugAlreadyExistsException,
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=list[Category])
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
    except CategoryNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())


@router.get("/slug/{slug}", response_model=Category)
async def get_category_by_slug(
    slug: str,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
):
    try:
        return await use_cases.get_by_slug(slug)
    except CategoryNotFoundBySlugException as e:
        raise NotFoundException(detail=e.get_detail())


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(
    category_data: CategoryCreate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
):
    try:
        return await use_cases.create(category_data)
    except CategorySlugAlreadyExistsException as e:
        raise ConflictException(detail=e.get_detail())


@router.put("/{id}", response_model=Category)
async def update_category(
    id: int,
    category_data: CategoryUpdate,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
):
    try:
        if not current_user.get("is_admin"):
            raise ForbiddenException(
                detail="Только администратор может редактировать категории"
            )

        return await use_cases.update(id, category_data)
    except CategoryNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())


@router.delete("/{id}")
async def delete_category(
    id: int,
    use_cases: CategoryUseCases = Depends(get_category_use_cases),
    current_user: dict = Depends(get_current_user),
):
    try:
        if not current_user.get("is_admin"):
            raise ForbiddenException(
                detail="Только администратор может удалять категории"
            )

        await use_cases.delete(id)
        return {"status": "success", "message": f"Category {id} deleted"}
    except CategoryNotFoundException as e:
        raise NotFoundException(detail=e.get_detail())
