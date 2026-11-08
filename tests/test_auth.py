async def register(client, email = "penis@example.com", password = "sosal671488"):
    await client.post("/users/register", json = {"email": email, "password": password})


async def login(client, email = "penis@example.com", password = "sosal671488"):
    return await client.post(
        "/auth/login", data = {"username": email, "password": password}
    )


async def test_login_success(client):
    await register(client)

    response = await login(client)

    assert response.status_code == 200
    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


async def test_login_wrong_password(client):
    await register(client)

    response = await login(client, password="wrong-password")

    assert response.status_code == 401


async def test_login_unknown_email(client):
    response = await login(client, email = "unknown_email@wrong.com")

    assert response.status_code == 401


async def test_login_errors_are_identical(client):
    await register(client)

    wrong_password = await login(client, password = "ShitAssHolePassword")
    wrong_email = await login(client, email = "ShitAssHoleEmail@Cock.com")

    assert wrong_password.json() == wrong_email.json()


async def test_me_without_token(client):
    response = await client.get(
        "/users/me"
    )

    assert response.status_code == 401



async def test_me_with_token(client):
    await register(client)
    token = (await login(client)).json()["access_token"]

    response = await client.get(
        "/users/me", headers = {"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "penis@example.com"



async def test_me_with_invalid_token(client):
    response = await client.get(
        "/users/me", headers = {"Authorization": "Bearer ruk.obl.udd"}
    )

    assert response.status_code == 401