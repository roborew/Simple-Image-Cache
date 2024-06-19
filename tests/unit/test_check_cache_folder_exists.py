from unittest.mock import patch

import pytest

from image_cache_app.utils.check_cache_folder_exists import check_cache_folder_exists


@patch("os.makedirs")
@patch("os.path.exists")
def test_check_cache_folder_exists_when_cache_dir_does_not_exist(
    mock_exists, mock_makedirs, client
):
    # Mock the exists function to return False
    mock_exists.return_value = False

    with client.application.app_context():
        check_cache_folder_exists(client.application)

    # Assert that the makedirs function was called
    mock_makedirs.assert_called_once_with(client.application.config["CACHE_DIR"])


@patch("os.makedirs")
@patch("os.path.exists")
def test_check_cache_folder_exists_when_cache_dir_exists(
    mock_exists, mock_makedirs, client
):
    # Mock the exists function to return True
    mock_exists.return_value = True

    with client.application.app_context():
        check_cache_folder_exists(client.application)

    # Assert that the makedirs function was not called
    mock_makedirs.assert_not_called()


@patch("os.makedirs")
@patch("os.path.exists")
def test_check_cache_folder_exists_raises_permission_error_when_creating_cache_dir(
    mock_exists, mock_makedirs, client
):
    # Mock the exists function to return False
    mock_exists.return_value = False
    # Mock the makedirs function to raise a PermissionError
    mock_makedirs.side_effect = PermissionError

    with client.application.app_context():
        with pytest.raises(PermissionError):
            check_cache_folder_exists(client.application)


@patch("os.makedirs")
@patch("os.path.exists")
def test_check_cache_folder_exists_raises_exception_when_creating_cache_dir(
    mock_exists, mock_makedirs, client
):
    # Mock the exists function to return False
    mock_exists.return_value = False
    # Mock the makedirs function to raise an Exception
    mock_makedirs.side_effect = Exception

    with client.application.app_context():
        with pytest.raises(Exception):
            check_cache_folder_exists(client.application)
