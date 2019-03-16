"""
All pymongo operations are LAZY
"""

from flask import current_app, g
import pymongo
from bson import BSON


def init_db(db_name):
    """
    Initialize MongoDB database into request's global instance

    :param db_name: string, name of database
    :return: pymongo Database object
    """
    if 'db' not in g:
        # connect to mongo db
        client = pymongo.MongoClient(current_app.config['MONGO_HOST'],
                                     current_app.config['MONGO_PORT'])
        g.db = client[db_name]
    return g.db


def insert_one(collection, document):
    """
    Insert a single document into given collection

    :param collection: pymongo collection object
    :param document: dict, key-value pair of data
    :return: id of inserted entry
    """
    return collection.insert_one(document).inserted_id



def find_all(collection, f=None):
    """
    Query a collection

    :param f: dict, filter for query, can be nested dict
    :return: pymongo cursor object, index like python dict
    """

    return collection.find(BSON.encode(f))



def delete_all(collection, f):
    """
    :return: number of documents deleted
    """
    return collection.delete_many(BSON.encode(f)).deleted_count



def update_all(collection, f, update):
    """
    :return: # of documents found and # of documents updated
    """
    result = collection.update_many(BSON.encode(f), BSON.encode(update))
    return result.matched_count, result.modified_count




