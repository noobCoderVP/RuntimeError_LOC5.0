from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import datetime


class Manuf(BaseModel):
    username: str = Field(...)
    company: str = Field(...)
    name: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    joinedAt: datetime.datetime = Field(default=datetime.datetime.now())
    ratings: List[int] = Field(default=[])

class updateManuf(BaseModel):
    username: Optional[str] 
    company: Optional[str]
    email: Optional[EmailStr] 
    name: Optional[str]
    password: Optional[str]
    ratings: Optional[List[int]]
