from fastapi import status


def test_register_user_returns_token_and_profile(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test", "email": "test@example.com", "password": "123456"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["expires_in"] > 0
    assert body["user"]["email"] == "test@example.com"
    assert body["user"]["is_active"] is True


def test_register_duplicate_email_returns_conflict(client):
    payload = {"name": "Test", "email": "dup@example.com", "password": "123456"}
    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == status.HTTP_201_CREATED

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == status.HTTP_409_CONFLICT
    assert second.json()["detail"] == "Email already registered"


def test_login_returns_user_payload(client):
    client.post(
        "/api/auth/register",
        json={"name": "Test", "email": "login@example.com", "password": "secret1"},
    )
    response = client.post(
        "/api/auth/login",
        data={"username": "login@example.com", "password": "secret1"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    body = response.json()
    assert body["user"]["email"] == "login@example.com"
    assert body["access_token"]
    assert body["expires_in"] > 0
