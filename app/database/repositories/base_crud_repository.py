from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type

from database.schemas.user_schema import UserUpdate, UserUpdatePartial
from database.schemas.user_task_schema import UserTaskUpdate, UserTaskUpdatePartial

ModelT = TypeVar("ModelT")
ModelDbHelper = TypeVar('ModelDbHelper')


class BaseCrudRepository(Generic[ModelT, ModelDbHelper], ABC):
    db_helper: ModelDbHelper

    @abstractmethod
    def get_user(self, user_telegram_id: int):
        raise NotImplementedError("get_user() is not implemented()")

    @abstractmethod
    def add_user(self, user_model: ModelT):
        raise NotImplementedError("add_user() is not implemented()")

    @abstractmethod
    def update_user(self,
                    user_model: ModelT,
                    user_update: UserUpdate | UserUpdatePartial,
                    partial: bool = False):
        raise NotImplementedError("update_user() is not implemented()")

    @abstractmethod
    def delete_user(self, user_model: ModelT):
        raise NotImplementedError("delete_user() is not implemented()")

    @abstractmethod
    def get_task(self, task_id: int):
        raise NotImplementedError("get_task() is not implemented()")

    @abstractmethod
    def add_task(self, task_model: ModelT):
        raise NotImplementedError("add_task() is not implemented()")

    @abstractmethod
    def update_task(self,
                    task_in: ModelT,
                    user_task_update: UserTaskUpdate | UserTaskUpdatePartial,
                    partial: bool = False):
        raise NotImplementedError("update_task() is not implemented()")

    @abstractmethod
    def delete_task(self, task_model: ModelT):
        raise NotImplementedError("delete_task() is not implemented()")

    def get_user_tasks(self, user_id: int):
        raise NotImplementedError("get_user_tasks() is not implemented()")

