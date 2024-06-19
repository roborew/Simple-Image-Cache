import hashlib
import os

from flask import current_app

from image_cache_app.cache.cache_manager import CacheManager
from image_cache_app.processing.image_processing_factory import ImageProcessingFactory
from image_cache_app.storage.image_loader import ImageLoader
from image_cache_app.utils.check_cache_folder_exists import check_cache_folder_exists
from image_cache_app.utils.image_path_location import image_path_location
from image_cache_app.utils.url_parser import parse_url
from image_cache_app.utils.validate_hmac import ValidateHmac


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

    def cache_image(self):
        """
        Caches an image.
        It first checks if the cache directory exists and creates it if it doesn't.
        Then it caches the image and returns the path to the cached image.
        If the image file does not exist, it logs an error and returns a path to a default image.
        """
        params = parse_url(self.url)

        # The following does nothing for now, but for future security enhancements
        if ValidateHmac.validate(params["hmac_key"]):
            # Remove the HMAC key from the params as no longer needed
            del params["hmac_key"]
        else:
            raise ValueError("Invalid HMAC")

        if not isinstance(params, dict) or "image_path" not in params:
            raise ValueError(
                "Invalid parameters. 'params' must be a dictionary containing the key 'image_path'."
            )
        image_path = image_path_location(
            current_app.config["IMAGE_DIR"], params["image_path"]
        )
        del params["image_path"]

        try:
            # Check cache folder exists
            check_cache_folder_exists(current_app)
            # Load the image from storage if not in cache
            image_loader = ImageLoader(image_path)
            image = image_loader.load_image()

            factory = ImageProcessingFactory()
            file_type = current_app.config["IMAGE_FORMAT_DEFAULT"]
            quality = current_app.config["IMAGE_QUALITY_DEFAULT"]

            for action, action_params in params.items():
                strategy = factory.get_process_strategy(action)
                if action == "file_type":
                    image, file_type = strategy.process(image, action_params)
                elif action == "compression":
                    image, quality = strategy.process(image, action_params)
                else:
                    image = strategy.process(image, action_params)

            # Save the processed image to a temporary file and cache it
            image_name = f"{self.cache_key}.{file_type}"
            cached_image_path = os.path.join(
                current_app.config["CACHE_DIR"], image_name
            )
            factory.processor.save(image, cached_image_path, file_type, quality)
            self.cacheManager.set(self.cache_key, image_name)
            return cached_image_path
        except FileNotFoundError:
            current_app.logger.warn(f"Image not found:  {image_path}")
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
