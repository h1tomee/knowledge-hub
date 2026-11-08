async def test_health(client):
    responce = await client.get("/healt")


    assert responce.status_code == 200
    assert responce.json() == {"status": "ok"}