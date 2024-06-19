import os

from dotenv import load_dotenv
from flask import Flask

from image_cache_app import routes

load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["IMAGE_DIR"] = os.getenv("IMAGE_DIR")
    app.config["CACHE_DIR"] = os.getenv("CACHE_DIR")
    app.config["IMAGE_FORMAT_DEFAULT"] = os.getenv("IMAGE_FORMAT_DEFAULT")
    app.config["IMAGE_QUALITY_DEFAULT"] = os.getenv("IMAGE_QUALITY_DEFAULT")
    if config:
        app.config.update(config)
    with app.app_context():
        app.register_blueprint(routes.bp)
    return app
