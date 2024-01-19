from pydantic import BaseModel, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] | None = None
    password: Optional[str] | None = None


class User(UserBase):
    id: int
    hashed_password: str
    is_active: bool
    is_super_user: bool

    model_config = ConfigDict(from_attributes=True)
