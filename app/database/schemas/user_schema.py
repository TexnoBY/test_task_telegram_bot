from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    login: str
    user_telegram_id: int
    name: str
    password: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserUpdatePartial(UserCreate):
    login: str | None = None
    user_telegram_id: int | None = None
    name: str | None = None
    password: str | None = None


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
