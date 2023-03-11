from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
import datetime


class Retailer(BaseModel):
    username: str = Field(...)
    company: str = Field(...)
    password: str = Field(...)
    email: EmailStr = Field(...)
    joinedAt: datetime.datetime = Field(default=datetime.datetime.now())
    orders: List[dict] = Field(default=[])


class updateRetailer(BaseModel):
    username: str
    company: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    orders: List[dict] = Field(default=[])
