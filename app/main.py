import asyncio

from sqlalchemy.util import await_only

from database.repositories.alchemy_repository import alchemy_repository
from database.schemas.user_schema import UserCreate
from database.schemas.user_task_schema import UserTaskCreate, UserTaskUpdate, UserTaskUpdatePartial


async def main():
    # print(await alchemy_repository.add_user(UserCreate(login='test3', user_telegram_id= 13, password='password')))
    # print(await alchemy_repository.delete_user(await alchemy_repository.get_user(user_telegram_id=12)))
    user_task = await alchemy_repository.add_task(UserTaskCreate(title='title', message='message', user_id=3))
    print(user_task)
    user_task = await alchemy_repository.get_task(task_id=user_task.id)
    print(user_task)
    user_task = await alchemy_repository.update_task(user_task, user_task_update=UserTaskUpdatePartial(title='title update'), partial=True)
    print(user_task)
    user_task = await alchemy_repository.get_task(task_id=user_task.id)
    print(user_task.title)
    print(await alchemy_repository.delete_task(user_task_in=user_task))

if __name__ == '__main__':
    asyncio.run(main())