from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.database import AsyncSessionLocal
from backend.models.transaction import Transaction
from backend.schemas.transaction_schema import TransactionCreate
from backend.services.fraud_service import FraudEngine
from backend.services.risk_service import RiskEngine

router = APIRouter()
fraud_engine = FraudEngine()
risk_engine = RiskEngine()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/transactions")
async def create_transaction(txn: TransactionCreate, db: AsyncSession = Depends(get_db)):
    new_txn = Transaction(**txn.dict())
    db.add(new_txn)
    await db.commit()
    await db.refresh(new_txn)

    fraud_result = fraud_engine.detect_fraud([txn.dict()])
    risk_result = risk_engine.calculate_risk(txn.amount, 0.5)

    return {
        "transaction": new_txn,
        "fraud_flagged": len(fraud_result) > 0,
        "risk": risk_result
    }