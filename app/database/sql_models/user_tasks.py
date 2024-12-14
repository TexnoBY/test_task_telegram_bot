from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins import UserRelationMixin


class UserTasks(UserRelationMixin, Base):
    __tablename__ = 'user_tasks'
    _user_back_populates = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    message: Mapped[str]

