from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.database import get_db
from src.dependencies.auth import get_current_user, get_current_admin_user
from src.schemas.location import Location, LocationCreate, LocationUpdate
from src.schemas.users import User
from src.domain.location.use_cases.get_locations import GetLocationsUseCase
from src.domain.location.use_cases.get_location import GetLocationUseCase
from src.domain.location.use_cases.get_location_by_name import GetLocationByNameUseCase
from src.domain.location.use_cases.get_published_locations import (
    GetPublishedLocationsUseCase,
)
from src.domain.location.use_cases.create_location import CreateLocationUseCase
from src.domain.location.use_cases.update_location import UpdateLocationUseCase
from src.domain.location.use_cases.delete_location import DeleteLocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=list[Location])
async def get_locations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetLocationsUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/published", response_model=list[Location])
async def get_published_locations(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetPublishedLocationsUseCase()
    return await use_case.execute(db, skip=skip, limit=limit)


@router.get("/{location_id}", response_model=Location)
async def get_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetLocationUseCase()
    return await use_case.execute(db, location_id)


@router.get("/name/{name}", response_model=Location)
async def get_location_by_name(
    name: str,
    db: AsyncSession = Depends(get_db),
):
    use_case = GetLocationByNameUseCase()
    return await use_case.execute(db, name)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Location)
async def create_location(
    location_data: LocationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = CreateLocationUseCase()
    result = await use_case.execute(db, location_data, current_user.id)
    await db.commit()
    return result


@router.put("/{location_id}", response_model=Location)
async def update_location(
    location_id: int,
    location_data: LocationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = UpdateLocationUseCase()
    result = await use_case.execute(
        db, location_id, location_data, current_user.id, current_user.is_admin
    )
    await db.commit()
    return result


@router.delete("/{location_id}")
async def delete_location(
    location_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    use_case = DeleteLocationUseCase()
    await use_case.execute(db, location_id, current_user.id, current_user.is_admin)
    await db.commit()
    return {"status": "success", "message": f"Location {location_id} deleted"}
