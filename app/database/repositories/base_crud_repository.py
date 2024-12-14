from abc import ABC, abstractmethod
from typing import TypeVar, Generic

ModelT = TypeVar("ModelT")
DbHelperT = TypeVar("DbHelperT")


class BaseCrudRepository(Generic[ModelT, DbHelperT], ABC):

    def __init__(self, db_helper: DbHelperT):
        self.db_helper = db_helper

    @abstractmethod
    def get_user(self, user_id):
        raise NotImplementedError("get_user() is not implemented()")

    @abstractmethod
    def add_user(self, user_model: ModelT):
        raise NotImplementedError("add_user() is not implemented()")

    @abstractmethod
    def update_user(self, user_model: ModelT, **update_values):
        raise NotImplementedError("update_user() is not implemented()")

    @abstractmethod
    def delete_user(self, user_model: ModelT):
        raise NotImplementedError("delete_user() is not implemented()")

    @abstractmethod
    def get_task(self, task_id):
        raise NotImplementedError("get_task() is not implemented()")

    @abstractmethod
    def add_task(self, task_model: ModelT):
        raise NotImplementedError("add_task() is not implemented()")

    @abstractmethod
    def update_task(self, task_model: ModelT, **update_values):
        raise NotImplementedError("update_task() is not implemented()")

    @abstractmethod
    def delete_task(self, task_model: ModelT):
        raise NotImplementedError("delete_task() is not implemented()")

    def get_user_tasks(self, user_id):
        raise NotImplementedError("get_user_tasks() is not implemented()")

