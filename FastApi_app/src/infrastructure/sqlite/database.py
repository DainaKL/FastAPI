from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker


class Base(DeclarativeBase):
    pass


class Database:
    def __init__(self, db_url: str = "sqlite:///./db.sqlite3"):
        self._db_url = db_url
        self._engine = create_engine(
            self._db_url, connect_args={"check_same_thread": False}
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


database = Database()


def get_db() -> Session:
    with database.session() as session:
        yield session
