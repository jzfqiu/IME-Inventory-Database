from flask import Flask
from web import config
import pymongo


def create_app():
    # create and configure the app from config.py
    app = Flask(__name__)
    app.config.from_object(config.Config)

    from . import db, edit, search
    with app.app_context():
        db.get_db()
    app.register_blueprint(edit.edit_bp)
    app.register_blueprint(search.search_bp)

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'hello'

    @app.route('/test')
    def test():
        mongo_host = app.config['MONGO_HOST']
        mongo_port = int(app.config['MONGO_PORT'])
        mongo_username = app.config['MONGO_INITDB_ROOT_USERNAME']
        mongo_password = app.config['MONGO_INITDB_ROOT_PASSWORD']
        client = pymongo.MongoClient(host=mongo_host,
                                     port=mongo_port,
                                     username=mongo_username,
                                     password=mongo_password,
                                     serverSelectionTimeoutMS=1000)
        collection = client['db']['inventory']
        return 'test'

    return app
