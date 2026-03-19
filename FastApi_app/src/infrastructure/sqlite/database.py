from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from sqlalchemy.orm import DeclarativeBase


# Создаем базовый класс для моделей
class Base(DeclarativeBase):
    pass

class Database:
    def __init__(self, db_url: str = "sqlite:///./db.sqlite3"):
        self._db_url = db_url
        self._engine = create_engine(
            self._db_url,
            connect_args={"check_same_thread": False}  # Для SQLite
        )

    @contextmanager
    def session(self):
        #Контекстный менеджер для работы с сессией
        connection = self._engine.connect()
        
        Session = sessionmaker(bind=self._engine)
        session = Session()
        
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
            connection.close()

    def get_session(self):
        #Генератор для FastAPI Depends
        with self.session() as session:
            yield session


# Создаем глобальный экземпляр Database
database = Database()

# Функция для получения сессии (для Depends)
def get_db() -> Session:
    with database.session() as session:
        yield session
