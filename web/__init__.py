from flask import Flask
from web import config


def create_app():
    # create and configure the app from config.py
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from . import db
    db.init_db()

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'hello'

    return app