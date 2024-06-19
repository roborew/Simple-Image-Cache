from .image_processing_bridge import OpenCVImageProcessor
from .strategies.compression_strategy import CompressionStrategy
from .strategies.crop_strategy import CropStrategy
from .strategies.file_type_strategy import FileTypeStrategy
from .strategies.resize_strategy import ResizeStrategy


class ImageProcessingFactory:
    def __init__(self):
        self.processor = OpenCVImageProcessor()

    def get_process_strategy(self, action):
        if action == "resize":
            return ResizeStrategy(self.processor)
        elif action == "crop":
            return CropStrategy(self.processor)
        elif action == "file_type":
            return FileTypeStrategy(self.processor)
        elif action == "compression":
            return CompressionStrategy(self.processor)
