from .strategy import Strategy


class ResizeStrategy(Strategy):
    def process(self, image, params):
        width, height = params
        return self.processor.resize(image, width, height)
