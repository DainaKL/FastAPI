from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.api.depends import get_location_use_cases
from src.dependencies.auth import get_current_user
from src.domain.location.use_cases.location_use_cases import LocationUseCases
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.schemas.users import User
from src.core.exceptions.api_exceptions import (
    NotFoundException,
    LocationForbiddenException,
    InvalidIDException,
)

router = APIRouter(prefix="/locations", tags=["Locations"])


def validate_id(id: int) -> int:
    if id <= 0:
        raise InvalidIDException(id)
    return id


@router.get("/", response_model=list[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_all(db, skip=skip, limit=limit)


@router.get("/published", response_model=list[Location])
async def get_published_locations(
    skip: int = 0,
    limit: int = 100,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    db: AsyncSession = Depends(get_db),
):
    return await use_cases.get_published(db, skip=skip, limit=limit)


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    db: AsyncSession = Depends(get_db),
):
    validate_id(location_id)
    try:
        return await use_cases.get_by_id(db, location_id)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.get("/name/{name}", response_model=Location)
async def get_location_by_name(
    name: str,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await use_cases.get_by_name(db, name)
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    location_data: LocationCreate,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user.is_admin:
        raise LocationForbiddenException(action="создавать")
    result = await use_cases.create(db, location_data)
    await db.commit()
    return result


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(location_id)
    if not current_user.is_admin:
        raise LocationForbiddenException(action="редактировать")
    try:
        result = await use_cases.update(db, location_id, location_data)
        await db.commit()
        return result
    except Exception as e:
        raise NotFoundException(detail=str(e))


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    use_cases: LocationUseCases = Depends(get_location_use_cases),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    validate_id(location_id)
    if not current_user.is_admin:
        raise LocationForbiddenException(action="удалять")
    await use_cases.delete(db, location_id)
    await db.commit()
    return {"status": "success", "message": f"Location {location_id} deleted"}