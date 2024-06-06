def test_image_cache(client):
    response = client.get("/rs:200:200/s:4/test_image.jpeg")
    assert response.status_code == 200
