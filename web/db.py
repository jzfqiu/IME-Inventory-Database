"""
All pymongo operations are LAZY
"""

from flask import current_app, g
import pymongo


def get_db(db_name='db'):
    """
    Initialize MongoDB database into request's global instance

    :param db_name: string, name of database
    :return: pymongo Database object
    """
    if not 'db' in g:
        # connect to mongo db
        mongo_host = current_app.config['MONGO_HOST']
        mongo_port = int(current_app.config['MONGO_PORT'])
        mongo_username = current_app.config['MONGO_INITDB_ROOT_USERNAME']
        mongo_password = current_app.config['MONGO_INITDB_ROOT_PASSWORD']
        client = pymongo.MongoClient(host=mongo_host,
                                     port=mongo_port,
                                     username=mongo_username,
                                     password=mongo_password,
                                     serverSelectionTimeoutMS=1000)
        g.db = client[db_name]
    return g.db
