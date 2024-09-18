def get_user_id_and_token(client, username="testuser"):
    register_response = client.post(
        "/api/users/register",
        json={
            "username": username,
            "email": f"{username}@test.de",
            "password": "testpassword",
        },
    )
    login_response = client.post(
        "/api/users/login",
        data={"username": f"{username}@test.de", "password": "testpassword"},
    )
    token = login_response.json()["access_token"]

    return token, register_response.json()["id"]
