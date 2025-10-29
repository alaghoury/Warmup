from fastapi import status


def login(client, username, password):
    response = client.post(
        "/api/auth/login",
        data={"username": username, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == status.HTTP_200_OK
    return response.json()["access_token"]


def test_admin_can_list_users(client):
    client.post(
        "/api/auth/register",
        json={"name": "Regular", "email": "regular@example.com", "password": "secret1"},
    )
    token = login(client, "mohammedalaghoury@gmail.com", "Moh2611")
    response = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_200_OK
    emails = [user["email"] for user in response.json()]
    assert "regular@example.com" in emails


def test_non_admin_cannot_access_admin_routes(client):
    register = client.post(
        "/api/auth/register",
        json={"name": "User", "email": "user@example.com", "password": "secret2"},
    )
    assert register.status_code == status.HTTP_201_CREATED
    token = login(client, "user@example.com", "secret2")
    response = client.get("/api/admin/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_stats_reflect_user_activity(client):
    token = login(client, "mohammedalaghoury@gmail.com", "Moh2611")

    headers = {"Authorization": f"Bearer {token}"}

    initial = client.get("/api/admin/stats", headers=headers)
    assert initial.status_code == status.HTTP_200_OK
    initial_body = initial.json()
    assert initial_body["total_users"] >= 1
    assert initial_body["active_users"] >= 1

    created = client.post(
        "/api/auth/register",
        json={"name": "Activity", "email": "activity@example.com", "password": "secret3"},
    )
    assert created.status_code == status.HTTP_201_CREATED
    user_id = created.json()["user"]["id"]

    after_create = client.get("/api/admin/stats", headers=headers)
    assert after_create.status_code == status.HTTP_200_OK
    after_create_body = after_create.json()
    assert after_create_body["total_users"] == initial_body["total_users"] + 1
    assert after_create_body["active_users"] == initial_body["active_users"] + 1
    assert after_create_body["recent_signups"] >= initial_body["recent_signups"]

    deactivate = client.post(f"/api/admin/users/{user_id}/deactivate", headers=headers)
    assert deactivate.status_code == status.HTTP_200_OK

    after_deactivate = client.get("/api/admin/stats", headers=headers)
    assert after_deactivate.status_code == status.HTTP_200_OK
    after_deactivate_body = after_deactivate.json()
    assert after_deactivate_body["active_users"] == after_create_body["active_users"] - 1
