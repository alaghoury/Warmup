from fastapi import status


def test_register_user(client):
    response = client.post(
        "/api/auth/register",
        json={"name": "Test", "email": "test@example.com", "password": "123456"},
    )
    assert response.status_code == status.HTTP_201_CREATED
    body = response.json()
    assert "access_token" in body and body["access_token"]
    assert body["token_type"] == "bearer"


def test_register_duplicate_email_returns_conflict(client):
    payload = {"name": "Test", "email": "dup@example.com", "password": "123456"}
    first = client.post("/api/auth/register", json=payload)
    assert first.status_code == status.HTTP_201_CREATED

    second = client.post("/api/auth/register", json=payload)
    assert second.status_code == status.HTTP_409_CONFLICT
    assert second.json()["detail"] == "Email already registered"
