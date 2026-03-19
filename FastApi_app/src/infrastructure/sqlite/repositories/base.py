from typing import TypeVar, Generic, Type, Optional, List

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.infrastructure.sqlite.database import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model
    
    def get_by_id(self, id: int) -> Optional[ModelType]:
        return self.session.get(self.model, id)
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        return list(self.session.execute(stmt).scalars().all())
    
    def create(self, **kwargs) -> ModelType:
        obj = self.model(**kwargs)
        self.session.add(obj)
        # Не коммитим здесь - коммит будет в контекстном менеджере Database
        self.session.flush()
        self.session.refresh(obj)
        return obj
    
    def update(self, id: int, **kwargs) -> Optional[ModelType]:
        obj = self.get_by_id(id)
        if obj:
            for key, value in kwargs.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            self.session.flush()
            self.session.refresh(obj)
        return obj
    
    def delete(self, id: int) -> Optional[ModelType]:
        obj = self.get_by_id(id)
        if obj:
            self.session.delete(obj)
            self.session.flush()
        return obj
