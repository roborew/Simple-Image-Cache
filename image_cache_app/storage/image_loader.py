import os
from urllib.request import Request, urlopen

import cv2
import numpy as np


class ImageLoader:
    """
    A class used to load images from a given path.

    ...

    Attributes
    ----------
    image_path : str
        a string representing the path of the image

    Methods
    -------
    load_image():
        Loads the image from the given path.
    """

    def __init__(self, image_path):
        """
        Constructs all the necessary attributes for the ImageLoader object.

        Parameters
        ----------
            image_path : str
                a string representing the path of the image
        """
        self.image_path = image_path

    def load_image(self):
        """
        Loads the image from the given path.

        If the image path is a URL, it sends a request to the URL with a User-Agent header and reads the image from the response.
        If the image path is a local file path, it uses cv2.imread() to read the image.
        If the image path is neither a local file path nor a URL, it raises a FileNotFoundError.

        Returns
        -------
        image
            a numpy array representing the image
        """
        if self.image_path.startswith("https://") or self.image_path.startswith(
            "http://"
        ):
            req = Request(self.image_path, headers={"User-Agent": "Mozilla/5.0"})
            resp = urlopen(req)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            return cv2.imdecode(image, cv2.IMREAD_COLOR)  # The image object
        elif os.path.exists(self.image_path):
            return cv2.imread(self.image_path)
        else:
            raise FileNotFoundError(
                f"The image at {self.image_path} could not be read."
            )
