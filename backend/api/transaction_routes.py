from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.services.analytics_service import AnalyticsEngine
from backend.core.database import AsyncSessionLocal
from backend.models.transaction import Transaction
from backend.schemas.transaction_schema import TransactionCreate
from backend.services.fraud_service import FraudEngine
from backend.services.risk_service import RiskEngine
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.core.security import SECRET_KEY, ALGORITHM

router = APIRouter()
fraud_engine = FraudEngine()
risk_engine = RiskEngine()
analytics_engine = AnalyticsEngine()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

def require_role(required_role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        if user.get("role") != required_role:
            raise HTTPException(status_code=403, detail="Access denied")
        return user
    return role_checker

@router.post("/transactions")
async def create_transaction(
    txn: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(require_role("admin"))
):
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

@router.get("/customers/{customer_id}/analytics")
async def get_customer_analytics(
    customer_id: str,
    db: AsyncSession = Depends(get_db),
    user: dict = Depends(require_role("analyst"))
):

    result = await db.execute(
        select(Transaction).where(Transaction.customer_id == customer_id)
    )

    transactions = result.scalars().all()

    transaction_data = [
        {
            "amount": t.amount,
            "timestamp": t.timestamp
        } for t in transactions
    ]

    analytics = analytics_engine.generate_customer_analytics(transaction_data)

    return analytics