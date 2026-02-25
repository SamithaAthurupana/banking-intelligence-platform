from sqlalchemy import Column, Integer, String, Float, DateTime

import datetime

from backend.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(String, index=True)
    amount = Column(Float)
    merchant = Column(String)
    location = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)