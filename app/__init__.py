from flask import Flask
import logging


def create_app():
    app = Flask(__name__)
    logging.basicConfig(level=logging.INFO)

    from .routes import bp
    app.register_blueprint(bp)

    return app