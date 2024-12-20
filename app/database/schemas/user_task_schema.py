from pydantic import BaseModel, ConfigDict


class UserTaskBase(BaseModel):
    title: str
    message: str
    user_id: int


class UserTaskCreate(UserTaskBase):
    is_done: bool = False


class UserTaskUpdate(UserTaskBase):
    pass


class UserTaskUpdatePartial(UserTaskCreate):
    title: str | None = None
    message: str | None = None
    user_id: int | None = None
    is_done: bool | None = None


class UserTask(UserTaskBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_done: bool
