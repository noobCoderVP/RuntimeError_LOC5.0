from typing import Optional
from pydantic import BaseModel, EmailStr, Field
import datetime


class User(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    joinedAt: datetime.datetime = Field(...)
    profession: str = Field(...)
    password: str = Field(...)
    gender: bool = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Vaibhav patel",
                "email": "vaibhavpatel02892@gmail.com",
                "joinedAt": datetime.datetime.now(),
                "profession": "teacher",
                "password": "abcdefg",
                "gender": True,
            }
        }


class updateUser(BaseModel):
    email: Optional[EmailStr]
    name: Optional[str]
    profession: Optional[str]
    password: Optional[str]
    gender: Optional[str]
