from pydantic import BaseModel
from datetime import datetime

class TransactionCreate(BaseModel):
    customer_id: str
    amount: float
    merchant: str
    location: str
    timestamp: datetime

class TransactionResponse(TransactionCreate):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
