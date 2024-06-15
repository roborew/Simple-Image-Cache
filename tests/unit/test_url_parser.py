from sympy.testing import pytest

from image_cache_app.utils.url_parser import parse_url


def test_parse_url_with_all_parameters(client):
    url = "insecure/rs:100:100/c:10:10/ft:webp/cp:90/test_image.jpeg"
    expected_params = {
        "hmac_key": "insecure",
        "resize": (100, 100),
        "crop": (10, 10),
        "file_type": "webp",
        "compression": 90,
        "image_path": "test_image.jpeg",
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
