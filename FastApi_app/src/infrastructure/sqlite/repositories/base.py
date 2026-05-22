from typing import Generic, List, Type, TypeVar
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.sqlite.database import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get_by_id(self, session: AsyncSession, id: int) -> ModelType | None:
        return await session.get(self.model, id)

    async def get_all(
        self, session: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, session: AsyncSession, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        session.add(obj)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def update(
        self, session: AsyncSession, id: int, **kwargs
    ) -> ModelType | None:
        obj = await self.get_by_id(session, id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            await session.flush()
            await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        obj = await self.get_by_id(session, id)
        if obj:
            await session.delete(obj)
            await session.flush()
            return True
        return False
