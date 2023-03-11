from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import datetime


class User(BaseModel):
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    joinedAt: datetime.datetime = Field(default=datetime.datetime.now())
    password: str = Field(...)
    orders: List[dict] | None = Field(default=None)


class updateUser(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]
