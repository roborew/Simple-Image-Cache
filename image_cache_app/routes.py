from flask import (
    Blueprint,
    render_template,
    send_from_directory,
    current_app,
    send_file,
)

from image_cache_app.image_processor import ImageProcessor

bp = Blueprint("routes", __name__)


@bp.route("/")
def index():
    return render_template("pages/index.html")


@bp.route("/image/<path:filename>")
def serve_image(filename):
    image_dir = current_app.config["IMAGE_DIR"]
    return send_from_directory(image_dir, filename)


@bp.route("/cache/<path:filename>")
def serve_cache_image(filename):
    image_dir = current_app.config["CACHE_DIR"]
    return send_from_directory(image_dir, filename)


@bp.route("/<path:url>")
def image_cache(url):
    processor = ImageProcessor(url)
    image = processor.process()
    return send_file(image)
