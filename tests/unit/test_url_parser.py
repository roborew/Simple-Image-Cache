from sympy.testing import pytest

from image_cache_app.utils.url_parser import parse_url


def test_parse_url_with_all_parameters(client):
    url = "insecure/rs:100:100/c:10:10:10:10/ft:webp/cp:90/ft:webp/test_image.jpeg"
    expected_params = {
        "compression": 90,
        "crop": (10, 10, 10, 10),
        "file_type": "webp",
        "hmac_key": "insecure",
        "image_path": "test_image.jpeg",
        "resize": (100, 100),
    }
    assert parse_url(url) == expected_params


def test_parse_url_with_remote_url(client):
    url = "/insecure/rs:400:400/ft:jpg/cp:90/https://images.pexels.com/photos/1330219/pexels-photo-1330219.jpeg"
    expected_params = {
        "compression": 90,
        "file_type": "jpg",
        "hmac_key": "",
        "image_path": "https://images.pexels.com/photos/1330219/pexels-photo-1330219.jpeg",
        "resize": (400, 400),
    }
    assert parse_url(url) == expected_params


def test_parse_url_with_no_parameters(client):
    url = "insecure/test_image.jpeg"
    expected_params = {"hmac_key": "insecure", "image_path": "test_image.jpeg"}
    assert parse_url(url) == expected_params


def test_parse_url_with_invalid_resize_parameter(client):
    url = "insecure/rs:100a:100b/test_image.jpeg"
    with pytest.raises(ValueError):
        parse_url(url)


def test_parse_url_with_invalid_crop_parameter(client):
    url = "insecure/c:10a:10b/test_image.jpeg"
    with pytest.raises(ValueError):
        parse_url(url)


def test_parse_url_with_invalid_compression_parameter(client):
    url = "insecure/cp:90a/test_image.jpeg"
    with pytest.raises(ValueError):
        parse_url(url)
