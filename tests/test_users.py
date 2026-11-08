async def test_register_success(client):
    response = await client.post(
        "/users/register",
        json = {"email": "penis@example.com", "password": "sosal671488"},
    )


    assert response.status_code == 201
    data = response.json()
    assert data["is_active"] == True
    assert data["email"] == "penis@example.com"
    assert "password" not in data
    assert "hashed_password" not in data



async def test_register_duplicate_email(client):
    body = {"email": "penis@example.com", "password": "sosal671488"}
    await client.post("/users/register", json = body)


    response = await client.post("/users/register", json = body)


    assert response.status_code == 409



async def test_register_email_is_case_insensitive(client):


    await client.post(
        "/users/register",
        json = {"email": "penis@example.com", "password": "sosal671488"},
    )



    response = await client.post(
        "/users/register",
        json = {"email": "PENIS@example.com", "password": "sosal671488"},
    )


    assert response.status_code == 409



async def test_register_short_password(client):
    response = await client.post(
        "/users/register",
        json = {"email": "penis@example.com", "password": "xyu"}
    )

    assert response.status_code == 422



async def test_register_uganda_email(client):
    response = await client.post(
        "/users/register",
        json = {"email": "uganda", "password": "sosal671488"}
    )

    assert response.status_code == 422