import re
from urllib.parse import urlparse


def extract_url(s):
    match = re.search("https?://[^\s]+", s)
    if match:
        return match.group()
    return None


def parse_url(url):
    parsed_url = urlparse(url)
    parts = parsed_url.path.split("/")
    params = {}
    params["hmac_key"] = parts[0]  # Ignored for now, but for future implementations
    params["image_path"] = extract_url(parsed_url.path) or parts[-1]
    for part in parts[:-1]:
        if part.startswith("rs:"):
            size = tuple(map(int, part[3:].split(":")))
            params["resize"] = size
        elif part.startswith("c:"):
            crop_params = tuple(map(int, part[2:].split(":")))
            params["crop"] = crop_params
        elif part.startswith("ft:"):
            file_type = part[3:]
            params["file_type"] = file_type
        elif part.startswith("cp:"):
            compression = int(part[3:])
            params["compression"] = compression
    return params
