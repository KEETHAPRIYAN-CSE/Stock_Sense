import pytest


def test_register_and_login(client):
    # 1. Register
    reg_payload = {
        "email": "manager@stocksense.com",
        "full_name": "Inventory Manager",
        "password": "securepassword123",
        "role": "INVENTORY_MANAGER",
    }
    reg_res = client.post("/api/auth/register", json=reg_payload)
    assert reg_res.status_code == 201
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["email"] == "manager@stocksense.com"
    assert reg_data["user"]["role"] == "INVENTORY_MANAGER"

    # Duplicate registration should fail
    dup_res = client.post("/api/auth/register", json=reg_payload)
    assert dup_res.status_code == 400

    # 2. Login
    login_payload = {
        "email": "manager@stocksense.com",
        "password": "securepassword123",
    }
    login_res = client.post("/api/auth/login", json=login_payload)
    assert login_res.status_code == 200
    login_data = login_res.json()
    token = login_data["access_token"]
    assert token is not None

    # 3. Invalid Login
    bad_login = client.post(
        "/api/auth/login",
        json={"email": "manager@stocksense.com", "password": "wrongpassword"},
    )
    assert bad_login.status_code == 401

    # 4. Get Current User /me
    me_res = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "manager@stocksense.com"

    # 5. Unauthorized access without token
    unauth_res = client.get("/api/auth/me")
    assert unauth_res.status_code == 401


def test_password_reset_flow(client):
    # Create user first
    client.post(
        "/api/auth/register",
        json={
            "email": "staff@stocksense.com",
            "full_name": "Warehouse Staff",
            "password": "initialpassword",
            "role": "WAREHOUSE_STAFF",
        },
    )

    # Request OTP
    forgot_res = client.post(
        "/api/auth/forgot-password", json={"email": "staff@stocksense.com"}
    )
    assert forgot_res.status_code == 200
    dev_otp = forgot_res.json().get("dev_otp")
    assert dev_otp is not None
    assert len(dev_otp) == 6

    # Attempt reset with wrong OTP
    bad_reset = client.post(
        "/api/auth/reset-password",
        json={
            "email": "staff@stocksense.com",
            "otp": "000000",
            "new_password": "newpassword123",
        },
    )
    assert bad_reset.status_code == 400

    # Reset with correct OTP
    good_reset = client.post(
        "/api/auth/reset-password",
        json={
            "email": "staff@stocksense.com",
            "otp": dev_otp,
            "new_password": "newpassword123",
        },
    )
    assert good_reset.status_code == 200

    # Old password should now fail
    old_login = client.post(
        "/api/auth/login",
        json={"email": "staff@stocksense.com", "password": "initialpassword"},
    )
    assert old_login.status_code == 401

    # New password should succeed
    new_login = client.post(
        "/api/auth/login",
        json={"email": "staff@stocksense.com", "password": "newpassword123"},
    )
    assert new_login.status_code == 200
