from fastapi import FastAPI

from backend.api.transaction_routes import router
from backend.core.database import engine, Base
from backend.api.auth_routes import router as auth_router

app = FastAPI(title="AI Banking Intelligence Platform")

app.include_router(router, prefix="/api")
app.include_router(auth_router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)