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


def process_item(item, n=None):
    """
    Helper function for cleaning searched result

    :param item: a document (dict) returned by find_one() or batch iteration
    :param n: number of entry needed in detailed ['data']
    :return: another dict with _id and name separated from other data
    """
    try:
        object_id = item.pop('_id')
        name = item.pop('name')
        if n:
            data = list(item.items())[:n]
        else:
            data = list(item.items())
    except KeyError:
        raise
    return {'id': object_id, 'name': name, 'data': data}