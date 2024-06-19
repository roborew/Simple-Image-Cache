# processing/bridge.py
import cv2


class ImageProcessorBridge:
    def resize(self, image, width, height):
        raise NotImplementedError

    def crop(self, image, x, y, w, h):
        raise NotImplementedError

    def save(self, image, path, file_type="png", quality=95):
        raise NotImplementedError


class OpenCVImageProcessor(ImageProcessorBridge):
    def resize(self, image, width, height):
        return cv2.resize(image, (width, height))

    def crop(self, image, x, y, w, h):
        return image[y : y + h, x : x + w]

    def save(self, image, path, file_type="png", quality="95"):
        quality = int(quality)
        if file_type in ["jpg", "jpeg"]:
            cv2.imwrite(path, image, [cv2.IMWRITE_JPEG_QUALITY, quality])
        elif file_type == "png":
            cv2.imwrite(path, image, [cv2.IMWRITE_PNG_COMPRESSION, round(quality / 10)])
        else:
            cv2.imwrite(path, image)
