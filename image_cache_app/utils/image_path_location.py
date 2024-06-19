import os


def image_path_location(image_dir, image_path):
    if image_path.startswith("https://") or image_path.startswith("http://"):
        return image_path
    else:
        return os.path.join(image_dir, image_path)
