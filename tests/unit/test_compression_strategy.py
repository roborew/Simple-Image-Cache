from unittest import TestCase
from unittest.mock import MagicMock

from image_cache_app.processing.strategies.compression_strategy import (
    CompressionStrategy,
)


class CompressionStrategyTests(TestCase):
    def setUp(self):
        self.mock_processor = MagicMock()
        self.strategy = CompressionStrategy(self.mock_processor)
        self.mock_image = MagicMock()

    def test_should_return_same_image_with_quality_when_process_called(self):
        result_image, result_quality = self.strategy.process(self.mock_image, 95)
        self.assertEqual(result_image, self.mock_image)
        self.assertEqual(result_quality, 95)

    def test_should_return_same_image_with_default_quality_when_no_quality_provided(
        self,
    ):
        result_image, result_quality = self.strategy.process(self.mock_image, None)
        self.assertEqual(result_image, self.mock_image)
        self.assertEqual(result_quality, None)
