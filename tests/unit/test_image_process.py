from unittest.mock import patch

from image_cache_app.image_processor import ImageProcessor


def test_check_cache_folder_exists_creates_directory_when_not_exists(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False), patch(
            "os.makedirs"
        ) as mock_makedirs:
            ImageProcessor.check_cache_folder_exists()
            mock_makedirs.assert_called_once()


def test_check_cache_folder_exists_does_not_create_directory_when_exists(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=True), patch(
            "os.makedirs"
        ) as mock_makedirs:
            ImageProcessor.check_cache_folder_exists()
            mock_makedirs.assert_not_called()


def test_cache_image_when_image_exists(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=True), patch(
            "image_cache_app.image_processor.CacheManager.set"
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.cache_image().endswith(".jpg")


def test_cache_image_when_image_does_not_exist(client):
    with client.application.app_context():
        with patch("os.path.exists", return_value=False):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.cache_image().endswith("image_not_found.svg")


def test_fetch_cache_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.CacheManager.get",
            return_value="test_image.jpg",
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.fetch_cache().endswith(".jpg")


def test_fetch_cache_when_cache_does_not_exist(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.CacheManager.get", return_value=None
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.fetch_cache() is None


def test_process_when_cache_exists(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache",
            return_value="test_image.jpg",
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.process().endswith(".jpg")


def test_process_when_cache_does_not_exist(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache",
            return_value=None,
        ), patch(
            "image_cache_app.image_processor.ImageProcessor.cache_image",
            return_value="test_image.jpg",
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.process().endswith(".jpg")


def test_process_when_fetch_cache_raises_exception(client):
    with client.application.app_context():
        with patch(
            "image_cache_app.image_processor.ImageProcessor.fetch_cache",
            side_effect=Exception("Test exception"),
        ), patch(
            "image_cache_app.image_processor.ImageProcessor.cache_image",
            return_value="test_image.jpg",
        ):
            processor = ImageProcessor(
                "http://127.0.0.1:5000/insecure/rs:100:100/s:4/test_image.jpeg"
            )
            assert processor.process().endswith(".jpg")
