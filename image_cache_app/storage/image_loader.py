import os

import cv2


class ImageLoader:
    def __init__(self, image_path):
        self.image_path = image_path

    def load_image(self):
        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"The image at {self.image_path} does not exist.")
        image = cv2.imread(self.image_path)
        if image is None:
            raise FileNotFoundError(
                f"The image at {self.image_path} could not be read."
            )
        return image
