from flask import Flask
from web import config


def create_app():
    # create and configure the app from config.py
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from . import search, edit
    app.register_blueprint(search.search_bp)
    app.register_blueprint(edit.edit_bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'hello'

    return app
