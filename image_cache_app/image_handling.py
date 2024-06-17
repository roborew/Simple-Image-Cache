import hashlib
import os

import cv2
from flask import current_app

from image_cache_app.cache.cache_manager import CacheManager
from image_cache_app.processing.image_processing_factory import ImageProcessingFactory
from image_cache_app.storage.image_loader import ImageLoader
from image_cache_app.utils.url_parser import parse_url


class ImageHandling:
    """
    The ImageProcessor class is responsible for handling image caching operations.
    It fetches cached images if they exist, and caches new images if they don't.
    """

    def __init__(self, url):
        """
        Initializes the ImageProcessor with a URL.
        The URL is used to generate a unique cache key using MD5 hashing.
        """
        self.url = url
        self.cache_key = hashlib.md5(self.url.encode()).hexdigest()
        self.cacheManager = CacheManager()

    @staticmethod
    def check_cache_folder_exists():
        """
        Checks if the cache directory exists, and creates it if it doesn't.
        The cache directory path is retrieved from the application's configuration.
        """
        cache_dir = current_app.config["CACHE_DIR"]
        try:
            if not os.path.exists(cache_dir):
                os.makedirs(cache_dir)
        except PermissionError:
            current_app.logger.error(
                f"Permission denied: Unable to create or access the directory {cache_dir}"
            )
        except Exception as e:
            current_app.logger.error(
                f"An error occurred while creating or accessing the directory {cache_dir}: {str(e)}"
            )

    def cache_image(self):
        """
        Caches an image.
        It first checks if the cache directory exists and creates it if it doesn't.
        Then it caches the image and returns the path to the cached image.
        If the image file does not exist, it logs an error and returns a path to a default image.
        """
        params = parse_url(self.url)
        if not isinstance(params, dict) or "image_path" not in params:
            raise ValueError(
                "Invalid parameters. 'params' must be a dictionary containing the key 'image_path'."
            )

        self.check_cache_folder_exists()
        image_path = os.path.join(current_app.config["IMAGE_DIR"], params["image_path"])
        # Load the image from storage if not in cache
        image_loader = ImageLoader(image_path)
        try:
            image = image_loader.load_image()

            for action, action_params in params.items():
                strategy = ImageProcessingFactory.get_process_strategy(action)
                image = strategy.process(image, action_params)

            image_name = f"{self.cache_key}.webp"
            cached_image_path = os.path.join(
                current_app.config["CACHE_DIR"], image_name
            )
            cv2.imwrite(cached_image_path, image)
            self.cacheManager.set(self.cache_key, cached_image_path)
            return cached_image_path
        except FileNotFoundError:
            current_app.logger.error(f"Image not found:  {image_path}")
            return os.path.join(current_app.config["IMAGE_DIR"], "image_not_found.svg")
        except Exception as e:
            current_app.logger.error(
                f"An error occurred while caching the image: {str(e)}"
            )
            return os.path.join(current_app.config["IMAGE_DIR"], "image_not_found.svg")

    def fetch_cache_image(self):
        """
        Fetches a cached image if it exists.
        If an error occurs during the fetch operation, it logs the error and returns an error response.
        """
        try:
            cached_image = self.cacheManager.get(self.cache_key)
            if cached_image:
                image_cache_path = os.path.join(
                    current_app.config["CACHE_DIR"], cached_image
                )
                return image_cache_path
            else:
                return None
        except Exception as e:
            current_app.logger.error(
                f"Error fetching cache and loading image: {str(e)}"
            )
            raise

    def process(self):
        """
        Processes an image request.
        It first tries to fetch a cached image. If a cached image is found, it returns it.
        If no cached image is found, it caches the image and returns the path to the cached image.
        If an error occurs while fetching the cache, it logs the error and attempts to cache the image.
        """
        try:
            cached_result = self.fetch_cache_image()
            if cached_result:
                return cached_result
            else:
                return self.cache_image()
        except Exception as e:
            current_app.logger.error(
                f"An error occurred while processing the image: {str(e)}"
            )
            return self.cache_image()
