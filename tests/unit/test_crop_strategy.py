from unittest import TestCase
from unittest.mock import MagicMock

from image_cache_app.processing.strategies.crop_strategy import CropStrategy


class CropStrategyTests(TestCase):
    def setUp(self):
        self.mock_processor = MagicMock()
        self.strategy = CropStrategy(self.mock_processor)
        self.mock_image = MagicMock()

    def test_should_crop_image_with_valid_params(self):
        self.mock_processor.crop.return_value = "cropped_image"
        result = self.strategy.process(self.mock_image, (10, 20, 30, 40))
        self.assertEqual(result, "cropped_image")
        self.mock_processor.crop.assert_called_once_with(
            self.mock_image, 10, 20, 30, 40
        )
