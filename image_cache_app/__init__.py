import os

from flask import Flask

from image_cache_app import routes


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.update(config)

    with app.app_context():

        app.register_blueprint(routes.bp)

        CACHE_DIR = "image_cache"
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)

    return app
