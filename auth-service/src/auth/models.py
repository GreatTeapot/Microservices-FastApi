from sqlalchemy import (Boolean, Integer, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.schemas import UserRead
# from src.auth.schemas import UserRead
from src.database import Base


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(length=320), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False, default="subscriber")


    def to_read_model(self) -> UserRead:
        return UserRead(
            id=self.id,
            email=self.email,
            is_active=self.is_active,
            is_superuser=self.is_superuser,
            is_verified=self.is_verified,
            role=self.role,
        )
