import uuid

import pytest

@pytest.mark.asyncio
async def test_create_transaction(client):

    username = f"admin_{uuid.uuid4().hex[:6]}"

    # Register + Login
    await client.post("/auth/register", json={
        "username": username,
        "password": "adminpass"
    })

    # 🔥 ADD THIS BLOCK
    from backend.core.database import AsyncSessionLocal
    from sqlalchemy import text

    async with AsyncSessionLocal() as session:
        await session.execute(
            text("UPDATE users SET role='admin' WHERE username=:u"),
            {"u": username},
        )
        await session.commit()

    login = await client.post("/auth/login", json={
        "username": username,
        "password": "adminpass"
    })

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await client.post(
        "/api/transactions",
        json={
            "customer_id": "C100",
            "amount": 20000,
            "merchant": "Amazon",
            "location": "Colombo",
            "timestamp": "2026-02-26T10:00:00"
        },
        headers=headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "risk" in data