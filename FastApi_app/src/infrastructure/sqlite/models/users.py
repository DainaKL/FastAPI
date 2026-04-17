from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String

from src.infrastructure.sqlite.database import Base


class User(Base):
    __tablename__ = "auth_user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    login: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
