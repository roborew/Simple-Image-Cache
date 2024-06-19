from .strategy import Strategy


class FileTypeStrategy(Strategy):
    def process(self, image, params):
        file_type = params
        return image, file_type
