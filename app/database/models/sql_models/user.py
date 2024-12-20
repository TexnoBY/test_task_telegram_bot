from typing import List, TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user_task import UserTask


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(unique=True, index=True)
    user_telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    name: Mapped[str]
    password: Mapped[str]

    tasks: Mapped[List["UserTask"]] = relationship(
        back_populates="user"
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, login={self.login!r}, user_telegram_id={self.user_telegram_id!r}, password={self.password!r})"

    def __repr__(self):
        return str(self)
