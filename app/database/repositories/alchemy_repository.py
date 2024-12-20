from sqlalchemy import select

from app.database.db_helpers.alchemydbhelper import AlchemyDBHelper, alchemy_db_helper
from app.database.models.sql_models import User, UserTask
from app.database.repositories.base_crud_repository import BaseCrudRepository
from app.database.schemas.user_schema import User as UserSchema, UserCreate, UserUpdate, UserUpdatePartial
from app.database.schemas.user_task_schema import UserTaskCreate, UserTaskUpdate, UserTaskUpdatePartial


class AlchemyRepository(BaseCrudRepository):
    db_helperL: AlchemyDBHelper

    def __init__(self, db_helper: AlchemyDBHelper):
        self.db_helper = db_helper

    async def add_user(self, user_in: UserCreate) -> User:
        """
        Добавить пользователя в бд

        @param user_in:
        @return:
        """
        user = User(**user_in.model_dump())
        async with self.db_helper.session_factory() as session:
            session.add(user)
            await session.commit()
            return user

    async def get_user(self, user_telegram_id: int) -> User | None:
        """
        Получить пользователя по telegram_id

        @param user_telegram_id:
        @return:
        """
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(User).where(User.user_telegram_id == user_telegram_id)
            )
            user: [User | None] = await session.scalar(stmt)

            return user

    async def check_unique_login(self, login: str) -> bool:
        """
        Проверить уникальность логина
        @param login:
        @return:
        """
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(User.login).where(User.login == login)
            )
            login: bool = (await session.scalar(stmt)) is not None

            return login

    async def update_user(self,
                          user_in: UserSchema,
                          user_update: UserUpdate | UserUpdatePartial,
                          partial: bool = False) -> User:
        """
        Обновить пользователя

        @param user_in:
        @param user_update:
        @param partial:
        @return:
        """
        async with self.db_helper.session_factory() as session:
            user = await session.scalar(select(User).where(User.id == user_in.id))
            for name, value in user_update.model_dump(exclude_unset=partial).items():
                setattr(user, name, value)
            await session.commit()
            return user

    async def delete_user(self, user_in: UserSchema) -> None:
        """
        Удалить пользователя

        @param user_in:
        """
        async with self.db_helper.session_factory() as session:
            await session.delete(user_in)
            await session.commit()

    async def add_task(self, task_in: UserTaskCreate):
        """
        Добавить задачу

        @param task_in:
        @return:
        """
        user_task = UserTask(**task_in.model_dump())
        async with self.db_helper.session_factory() as session:
            session.add(user_task)
            await session.commit()
            return user_task

    async def get_task(self, task_id: int) -> UserTask | None:
        """
        Добавить задачу в бд

        @param task_id:
        @return:
        """
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(UserTask).where(UserTask.id == task_id)
            )
            user_task: [UserTask | None] = await session.scalar(stmt)

            return user_task

    async def update_task(self,
                          task_in: UserTask,
                          user_task_update: UserTaskUpdate | UserTaskUpdatePartial,
                          partial: bool = False) -> UserTask:
        """
        Обновить задачу

        @param task_in:
        @param user_task_update:
        @param partial:
        @return:
        """
        async with self.db_helper.session_factory() as session:
            user_task = await session.scalar(select(UserTask).where(UserTask.id == task_in.id))
            for name, value in user_task_update.model_dump(exclude_unset=partial).items():
                setattr(user_task, name, value)
            await session.commit()
            return user_task

    async def delete_task(self, user_task_in: UserTask) -> None:
        """
        Удалить задачу

        @param user_task_in:
        """
        async with self.db_helper.session_factory() as session:
            await session.delete(user_task_in)
            await session.commit()

    async def get_user_tasks(self, telegram_user_id: int, offset: int = 0, limit: int = 10) -> list[UserTask]:
        """
        Получить список задач пользователя
        @param telegram_user_id:
        @param offset:
        @param limit:
        @return:
        """
        user = await self.get_user(telegram_user_id)
        async with self.db_helper.session_factory() as session:
            stmt = (
                select(UserTask).where(UserTask.user_id == user.id).offset(offset).limit(limit)
            )
            user_tasks = await session.scalars(stmt)
            return user_tasks


alchemy_repository = AlchemyRepository(db_helper=alchemy_db_helper)
