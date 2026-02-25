from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

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


@router.post("/transactions")
async def create_transaction(txn: TransactionCreate, db: AsyncSession = Depends(get_db)):
    # Fetch customer history
    result = await db.execute(
        select(Transaction).where(Transaction.customer_id == txn.customer_id)
    )
    history = result.scalars().all()

    history_data = [
        {
            "amount": t.amount,
            "timestamp": t.timestamp
        } for t in history
    ]

    fraud_result = fraud_engine.analyze(txn.dict(), history_data)

    risk_result = risk_engine.calculate_risk(
        txn.amount,
        fraud_result["anomaly_score"]
    )

    # Save transaction
    new_txn = Transaction(**txn.dict())
    db.add(new_txn)
    await db.commit()
    await db.refresh(new_txn)

    return {
        "transaction_id": new_txn.id,
        "fraud_flagged": fraud_result["fraud"],
        "risk": risk_result
    }