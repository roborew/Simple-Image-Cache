from flask import Blueprint

bp = Blueprint("routes", __name__)


@bp.route("/<path:url>")
def image_cache(url):
    return f"You entered: {url}"
