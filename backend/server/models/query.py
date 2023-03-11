from pydantic import BaseModel, EmailStr, Field, FilePath
from typing import List, Optional
import datetime


class Query(BaseModel):
    email: EmailStr = Field(...)
    timing: datetime.datetime = Field(default=datetime.datetime.now())
    description: str = Field(..., max_length=100)
    images: List[FilePath] = Field(default=[], max_items=5)


class updateQuery(BaseModel):
    email: Optional[EmailStr] = Field(...)
    description: Optional[str] = Field(..., max_length=100)
    images: Optional[List[FilePath]] = Field(default=[], max_items=5)
