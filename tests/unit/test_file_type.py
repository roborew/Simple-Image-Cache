from unittest import TestCase
from unittest.mock import MagicMock

from image_cache_app.processing.strategies.file_type_strategy import FileTypeStrategy


class FileTypeStrategyTests(TestCase):
    def setUp(self):
        self.mock_image = MagicMock()
        self.strategy = FileTypeStrategy(self.mock_image)

    def test_should_return_same_image_with_given_file_type(self):
        result_image, result_file_type = self.strategy.process(self.mock_image, "jpeg")
        self.assertEqual(result_image, self.mock_image)
        self.assertEqual(result_file_type, "jpeg")
