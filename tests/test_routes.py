from dotenv import load_dotenv

load_dotenv()


def test_image_cache(client):
    url = "http://127.0.0.1:8000/insecure/rs:100:100/test_image.jpeg"
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")


def test_image_cache_process(client):
    url = "http://127.0.0.1:5000/insecure/rs:100:100/test_image.jpeg"
    response = client.get(url)
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")


def test_image_request(client):
    response = client.get("/image/test_image.jpeg")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")


def test_cache_request(client):
    response = client.get("/cache/fac0246c37ae154d65ff76bf33eab256.png")
    assert response.status_code == 200
    assert response.headers["Content-Type"].startswith("image/")


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Simple Image Cache" in response.data
