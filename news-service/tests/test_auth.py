from conftest import client


def test_register():
    response = client.post("/api/v1/auth/register", json={
        "username": "mekaaaa",
        "email": "boysscall@gmail.com",
        "password": "gmail12345",
        "is_active": True,
        "is_superuser": False,
        "is_verified": False,
    })

    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_login():
    response = client.post("/api/v1/auth/login", json={
        "credential": "zaka@gmail.com",
        "password": "gmail12345"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

#
# def test_get_profile():
#     login_response = client.post("/api/v1/auth/login", json={
#         "credential": "kale@gmail.com",
#         "password": "gmail12345"
#     })
#     tokens = login_response.json()
#
#     profile_response = client.get("/api/v1/auth/profile", headers={
#         "Authorization": f"Bearer {tokens['access_token']}"
#     })
#
#     assert profile_response.status_code == 200
#
