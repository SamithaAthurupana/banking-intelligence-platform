from fastapi import FastAPI

from backend.api.transaction_routes import router
from backend.core.database import engine, Base

app = FastAPI(title="AI Banking Intelligence Platform")

app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)