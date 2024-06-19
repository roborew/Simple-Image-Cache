import os
from unittest.mock import patch

from sympy.testing import pytest

from image_cache_app.image_handling import ImageHandling


def test_cache_image_when_image_exists(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=True), patch(
            "image_cache_app.image_handling.CacheManager.set"
        ):
            processor = ImageHandling("insecure/rs:100:100/test_image.jpeg")
            assert processor.cache_image().endswith(".webp")


def test_cache_image_when_image_does_not_exist(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False):
            processor = ImageHandling("insecure/rs:100:100/test_image_not_exist.jpeg")
            result = processor.cache_image()
            assert result == os.path.join(
                client.application.config["IMAGE_DIR"], "image_not_found.svg"
            )


def test_fetch_cache_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_handling.CacheManager.get",
            return_value="test_image.webp",
        ):
            processor = ImageHandling("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.fetch_cache_image().endswith(".webp")


def test_process_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_handling.ImageHandling.fetch_cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageHandling("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")


def test_process_when_cache_does_not_exist(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_handling.ImageHandling.fetch_cache_image",
            return_value=None,
        ), patch(
            "image_cache_app.image_handling.ImageHandling.cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageHandling("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")


def test_process_when_fetch_cache_raises_exception(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_handling.ImageHandling.fetch_cache_image",
            side_effect=Exception("Test exception"),
        ), patch(
            "image_cache_app.image_handling.ImageHandling.cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageHandling("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")


def test_cache_image_when_makedirs_raises_permission_error(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False), patch(
            "os.makedirs", side_effect=PermissionError
        ):
            processor = ImageHandling("insecure/rs:100:100/test_image.jpeg")
            result = processor.cache_image()
            assert result == os.path.join(
                client.application.config["IMAGE_DIR"], "image_not_found.svg"
            )


def test_cache_image_when_makedirs_raises_exception(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False), patch(
            "os.makedirs", side_effect=Exception
        ):
            processor = ImageHandling("insecure/rs:100:100/test_image.jpeg")
            result = processor.cache_image()
            assert result == os.path.join(
                client.application.config["IMAGE_DIR"], "image_not_found.svg"
            )


def test_fetch_cache_when_cache_manager_get_raises_exception(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_handling.CacheManager.get", side_effect=Exception
        ):
            processor = ImageHandling("insecure/rs:100:100/test_image.jpeg")
            with pytest.raises(Exception):
                processor.fetch_cache_image()
