from pydantic import BaseModel,  Field
import datetime


class Transaction(BaseModel):
    doneby: str = Field(...)
    productId: str = Field(...)
    transactorid: str = Field(...)
    executedAt: datetime.datetime = Field(default=datetime.datetime.now())
    
