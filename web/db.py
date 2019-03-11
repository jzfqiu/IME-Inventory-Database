from flask import current_app, g


def get_db():
    if 'db' not in g:
        # connect to mongo db
        client = MongoClient(current_app.config['MONGO_HOST'],
                             current_app.config['MONGO_PORT'])

    return g.db


def close_db():
    # kick db out of global request instance
    db = g.pop('db', None)