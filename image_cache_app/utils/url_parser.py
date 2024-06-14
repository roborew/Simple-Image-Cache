from urllib.parse import urlparse


def parse_url(url):
    parsed_url = urlparse(url)
    path_components = parsed_url.path.split("/")
    parameters = {}
    parameters["hmac_key"] = path_components[0]
    parameters["image_path"] = path_components[-1]
    for component in path_components[1:-1]:
        if ":" in component:
            name, value = component.split(":", 1)
            parameters[name] = value
    return parameters
