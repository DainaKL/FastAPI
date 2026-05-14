import os
from contextlib import contextmanager
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()  # Загружаем переменные из .env


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str = None):
        if db_url is None:
            db_url = os.getenv("DATABASE_URL", "sqlite:///./db.sqlite3")
        self._db_url = db_url
        self._engine = create_engine(
            self._db_url, connect_args={"check_same_thread": False} if "sqlite" in self._db_url else {}
        )

    @contextmanager
    def session(self):
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
        with self.session() as session:
            yield session


# Создаем экземпляр Database с URL из переменных окружения
database = Database()


def get_db() -> Session:
    with database.session() as session:
        yield session