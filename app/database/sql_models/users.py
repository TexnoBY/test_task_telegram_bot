from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_tasks import UserTasks


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    tasks: Mapped[List["UserTasks"]] =  relationship(
        back_populates="owner",
        cascade="all, delete-orphan"
    )