import os
from unittest.mock import patch, MagicMock

import pytest

from image_cache_app.storage.image_loader import ImageLoader


@patch("cv2.imread")
def test_load_image_returns_image_when_image_exists(mock_imread):
    # Mock the imread function to return a non-None value
    mock_imread.return_value = MagicMock()

    image_loader = ImageLoader(os.path.join(os.getenv("IMAGE_DIR"), "test_image.jpeg"))
    image = image_loader.load_image()

    # Assert that the image was loaded successfully
    assert image is not None


@patch("cv2.imread")
def test_load_image_raises_file_not_found_error_when_image_does_not_exist(mock_imread):
    # Mock the imread function to return None
    mock_imread.return_value = None

    image_loader = ImageLoader("non_existing_image_path")

    # Assert that a FileNotFoundError is raised when the image does not exist
    with pytest.raises(FileNotFoundError):
        image_loader.load_image()


@patch("cv2.imdecode")
@patch("urllib.request.urlopen")
@patch("cv2.imread")
def test_load_image_returns_image_when_image_path_is_url(
    mock_imread, mock_urlopen, mock_imdecode
):
    # Mock the imread function to return None
    mock_imread.return_value = None
    # Mock the urlopen function to return a MagicMock
    mock_urlopen.return_value = MagicMock()
    # Mock the imdecode function to return a non-None value
    mock_imdecode.return_value = MagicMock()

    image_loader = ImageLoader(
        "https://images.pexels.com/photos/1330219/pexels-photo-1330219.jpeg"
    )
    image = image_loader.load_image()

    # Assert that the image was loaded successfully
    assert image is not None
