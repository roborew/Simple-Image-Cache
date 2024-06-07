def test_image_cache(client):
    response = client.get("/rs:200:200/s:4/test_image.jpeg")
    assert response.status_code == 200


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Image Cache Server Running" in response.data
