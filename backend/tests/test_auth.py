import pytest
import uuid

@pytest.mark.asyncio
async def test_register_and_login(client):

    username = f"testuser_{uuid.uuid4().hex[:6]}"
    # Register user
    response = await client.post("/auth/register", json={
        "username": username,
        "password": "testpass"
    })
    assert response.status_code == 200

    # Login
    response = await client.post("/auth/login", json={
        "username": username,
        "password": "testpass"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data