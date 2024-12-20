from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import UserRelationMixin


class UserTask(UserRelationMixin, Base):
    __tablename__ = 'user_task'
    _user_back_populates = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    message: Mapped[str]
    is_done: Mapped[bool] = mapped_column(default=False)
