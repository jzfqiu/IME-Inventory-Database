"""
All pymongo operations are LAZY
"""

from flask import current_app, g
import pymongo
from bson import BSON


# class MongoInstance():
#
#     def __init__(self, dbname='db'):
#         if not 'db' in g:
#             # connect to mongo db
#             mongo_host = current_app.config['MONGO_HOST']
#             mongo_port = int(current_app.config['MONGO_PORT'])
#             mongo_username = current_app.config['MONGO_INITDB_ROOT_USERNAME']
#             mongo_password = current_app.config['MONGO_INITDB_ROOT_PASSWORD']
#             client = pymongo.MongoClient(mongo_host, mongo_port,
#                                          username=mongo_username,
#                                          password=mongo_password,
#                                          authSource=db_name,
#                                          authMechanism='SCRAM-SHA-256',
#                                          serverSelectionTimeoutMS=1000)
#             g.db = client[db_name]


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
        client = pymongo.MongoClient(mongo_host, mongo_port,
                                     username=mongo_username,
                                     password=mongo_password,
                                     authSource=db_name,
                                     authMechanism='SCRAM-SHA-256',
                                     serverSelectionTimeoutMS=1000)
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


def insert_many(collection, documents):
    return collection.insert_many(documents).insert_ids


def find_all(collection, f=None):
    """
    Query a collection

    :param f: dict, filter for query, can be nested dict
    :return: pymongo cursor object, index like python dict
    """
    return collection.find(f)



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