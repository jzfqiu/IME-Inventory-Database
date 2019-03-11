from flask import Flask
from web import config


def create_app():
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(config.Config)

    # a simple page that says hello
    @app.route('/')
    def hello():
        return 'hello'

    return app