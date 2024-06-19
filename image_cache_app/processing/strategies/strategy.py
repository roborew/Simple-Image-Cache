from image_cache_app.processing.image_processing_bridge import ImageProcessorBridge


class Strategy:
    def __init__(self, processor: ImageProcessorBridge):
        self.processor = processor

    def process(self, image, params):
        pass
