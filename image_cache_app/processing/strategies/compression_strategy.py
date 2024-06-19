from .strategy import Strategy


class CompressionStrategy(Strategy):
    def process(self, image, params):
        quality = params
        return image, quality
