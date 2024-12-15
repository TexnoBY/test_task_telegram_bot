from sqlalchemy import select

from database.db_helpers.alchemydbhelper import AlchemyDBHelper, alchemy_db_helper
from database.models.sql_models import User, UserTask
from database.repositories.base_crud_repository import BaseCrudRepository
from database.schemas.user_schema import UserCreate, UserUpdate, UserUpdatePartial
from database.schemas.user_task_schema import UserTaskCreate, UserTaskUpdate, UserTaskUpdatePartial


class AlchemyRepository(BaseCrudRepository):
    db_helperL: AlchemyDBHelper

    def __init__(self, db_helper: AlchemyDBHelper):
        self.db_helper = db_helper

    async def add_user(self, user_in: UserCreate) -> User:
        user = User(**user_in.model_dump())
        async with self.db_helper.session_factory() as session:
            session.add(user)
            await session.commit()
            return user

    async def get_user(self, user_telegram_id: int) -> User | None :
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(User).where(User.user_telegram_id == user_telegram_id)
            )
            user: [User | None] = await session.scalar(stmt)

            return user

    async def update_user(self,
                          user_in: User,
                          user_update: UserUpdate | UserUpdatePartial,
                          partial: bool = False):
        async with self.db_helper.session_factory() as session:
            user = await session.scalar(select(UserTask).where(UserTask.id == user_in.id))
            for name, value in user_update.model_dump(exclude_unset=partial).items():
                setattr(user, name, value)
            await session.commit()
            return user

    async def delete_user(self, user_in: User):
        async with self.db_helper.session_factory() as session:
            await session.delete(user_in)
            await session.commit()

    async def add_task(self, task_in: UserTaskCreate):
        user_task = UserTask(**task_in.model_dump())
        async with self.db_helper.session_factory() as session:
            session.add(user_task)
            await session.commit()
            return user_task

    async def get_task(self, task_id: int):
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(UserTask).where(UserTask.id == task_id)
            )
            user_task: [UserTask | None] = await session.scalar(stmt)

            return user_task

    async def update_task(self,
                    task_in: UserTask,
                    user_task_update: UserTaskUpdate | UserTaskUpdatePartial,
                    partial: bool = False):
        async with self.db_helper.session_factory() as session:
            user_task = await session.scalar(select(UserTask).where(UserTask.id == task_in.id))
            for name, value in user_task_update.model_dump(exclude_unset=partial).items():
                setattr(user_task, name, value)
            await session.commit()
            return user_task

    async def delete_task(self, user_task_in: UserTask):
        async with self.db_helper.session_factory() as session:
            await session.delete(user_task_in)
            await session.commit()


alchemy_repository = AlchemyRepository(db_helper=alchemy_db_helper)


