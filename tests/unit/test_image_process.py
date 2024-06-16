import os
from unittest.mock import patch

from image_cache_app.image_processor import ImageProcessor


def test_cache_image_when_image_exists(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=True), patch(
            "image_cache_app.image_processor.CacheManager.set"
        ):
            processor = ImageProcessor("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.cache_image().endswith(".webp")


def test_cache_image_when_image_does_not_exist(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False):
            processor = ImageProcessor(
                "insecure/rs:100:100/s:4/test_image_not_exist.jpeg"
            )
            result = processor.cache_image()
            assert result == os.path.join(
                client.application.config["IMAGE_DIR"], "image_not_found.svg"
            )


def test_fetch_cache_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.CacheManager.get",
            return_value="test_image.webp",
        ):
            processor = ImageProcessor("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.fetch_cache_image().endswith(".webp")


def test_process_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageProcessor("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")


def test_process_when_cache_does_not_exist(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache_image",
            return_value=None,
        ), patch(
            "image_cache_app.image_processor.ImageProcessor.cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageProcessor("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")


def test_process_when_fetch_cache_raises_exception(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache_image",
            side_effect=Exception("Test exception"),
        ), patch(
            "image_cache_app.image_processor.ImageProcessor.cache_image",
            return_value="test_image.webp",
        ):
            processor = ImageProcessor("insecure/rs:100:100/s:4/test_image.jpeg")
            assert processor.process().endswith(".webp")
