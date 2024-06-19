from .strategy import Strategy


class CropStrategy(Strategy):
    def process(self, image, params):
        x, y, w, h = params
        return self.processor.crop(image, x, y, w, h)
