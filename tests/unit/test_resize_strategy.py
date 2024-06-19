from unittest import TestCase
from unittest.mock import MagicMock

from image_cache_app.processing.strategies.resize_strategy import ResizeStrategy


class ResizeStrategyTests(TestCase):
    def setUp(self):
        self.mock_processor = MagicMock()
        self.strategy = ResizeStrategy(self.mock_processor)
        self.mock_image = MagicMock()

    def test_should_resize_image_with_valid_params(self):
        self.mock_processor.resize.return_value = "resized_image"
        result = self.strategy.process(self.mock_image, (800, 600))
        self.assertEqual(result, "resized_image")
        self.mock_processor.resize.assert_called_once_with(self.mock_image, 800, 600)
