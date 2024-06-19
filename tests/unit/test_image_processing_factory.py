import unittest
from unittest.mock import patch, MagicMock

from image_cache_app.processing.image_processing_factory import ImageProcessingFactory
from image_cache_app.processing.strategies.compression_strategy import (
    CompressionStrategy,
)
from image_cache_app.processing.strategies.crop_strategy import CropStrategy
from image_cache_app.processing.strategies.file_type_strategy import FileTypeStrategy
from image_cache_app.processing.strategies.resize_strategy import ResizeStrategy


class TestImageProcessingFactory(unittest.TestCase):
    def setUp(self):
        self.factory = ImageProcessingFactory()

    @patch("image_cache_app.processing.image_processing_factory.ResizeStrategy")
    def test_should_return_resize_strategy_when_action_is_resize(
        self, mock_resize_strategy
    ):
        mock_resize_strategy.return_value = MagicMock(spec=ResizeStrategy)
        strategy = self.factory.get_process_strategy("resize")
        self.assertIsInstance(strategy, ResizeStrategy)

    @patch("image_cache_app.processing.image_processing_factory.CropStrategy")
    def test_should_return_crop_strategy_when_action_is_crop(self, mock_crop_strategy):
        mock_crop_strategy.return_value = MagicMock(spec=CropStrategy)
        strategy = self.factory.get_process_strategy("crop")
        self.assertIsInstance(strategy, CropStrategy)

    @patch("image_cache_app.processing.image_processing_factory.FileTypeStrategy")
    def test_should_return_file_type_strategy_when_action_is_file_type(
        self, mock_file_type_strategy
    ):
        mock_file_type_strategy.return_value = MagicMock(spec=FileTypeStrategy)
        strategy = self.factory.get_process_strategy("file_type")
        self.assertIsInstance(strategy, FileTypeStrategy)

    @patch("image_cache_app.processing.image_processing_factory.CompressionStrategy")
    def test_should_return_compression_strategy_when_action_is_compression(
        self, mock_compression_strategy
    ):
        mock_compression_strategy.return_value = MagicMock(spec=CompressionStrategy)
        strategy = self.factory.get_process_strategy("compression")
        self.assertIsInstance(strategy, CompressionStrategy)

    def test_should_return_none_when_action_is_unknown(self):
        strategy = self.factory.get_process_strategy("unknown")
        self.assertIsNone(strategy)
