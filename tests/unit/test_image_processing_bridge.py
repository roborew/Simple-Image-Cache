import unittest
from unittest.mock import patch, MagicMock

import cv2

from image_cache_app.processing.image_processing_bridge import OpenCVImageProcessor


class OpenCVImageProcessorTests(unittest.TestCase):
    def setUp(self):
        self.processor = OpenCVImageProcessor()
        self.mock_image = MagicMock()

    @patch.object(cv2, "resize")
    def test_should_resize_image_with_given_dimensions(self, mock_resize):
        mock_resize.return_value = "resized_image"
        result = self.processor.resize(self.mock_image, 100, 200)
        mock_resize.assert_called_once_with(self.mock_image, (100, 200))
        self.assertEqual(result, "resized_image")

    def test_should_crop_image_with_given_parameters(self):
        result = self.processor.crop(self.mock_image, 10, 20, 30, 40)
        self.mock_image.__getitem__.assert_called_once_with(
            (slice(20, 60), slice(10, 40))
        )
        self.assertEqual(result, self.mock_image.__getitem__.return_value)

    @patch.object(cv2, "imwrite")
    def test_should_save_image_with_given_path_and_file_type(self, mock_imwrite):
        self.processor.save(self.mock_image, "path/to/image", "png", 95)
        mock_imwrite.assert_called_once_with(
            "path/to/image",
            self.mock_image,
            [cv2.IMWRITE_PNG_COMPRESSION, round(95 / 10)],
        )
