from typing import Optional, List
from pydantic import BaseModel, Field
import datetime


class Product(BaseModel):
    productId: str = Field(...)
    manufracturer: str = Field(...)
    images: List[str] = Field(...)
    sentAt: datetime.datetime = Field(...)
    receivedAt: datetime.datetime | None = Field(default=None)
    received: bool = Field(default=False)


class updateProduct(BaseModel):
    images: Optional[List[str]] = Field(...)
    manufracturer: Optional[str] = Field(...)
    received: Optional[bool] = Field(default=False)
    receivedAt: Optional[datetime.datetime] | None = Field(default=None)
