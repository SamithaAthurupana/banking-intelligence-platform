import uuid

import pytest

@pytest.mark.asyncio
async def test_customer_analytics(client):

    username = f"analyst_{uuid.uuid4().hex[:6]}"

    await client.post("/auth/register", json={
        "username": username,
        "password": "password"
    })

    login = await client.post("/auth/login", json={
        "username": username,
        "password": "password"
    })

    token = login.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = await client.get(
        "/api/customers/C100/analytics",
        headers=headers
    )

    assert response.status_code in [200, 404]