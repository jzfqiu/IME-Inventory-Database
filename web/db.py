"""
All pymongo operations are LAZY
"""

from flask import current_app, g
import pymongo
from web.utils import *



def get_db(db_name='db'):
    """
    Initialize MongoDB database into request's global instance

    :param db_name: string, name of database

    :return: pymongo Database object
    """
    if 'db' not in g:
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


def unroll_cat(d, output_str=False):    
    """ helper function: unroll category information passed from js request
    
    Arguments:
        d {dict} -- json straight from request
        output_str {bool} -- [description] (default: {False})
    
    Returns:
        res {list of dict} -- list of flattened category information 
            to be fed into query builder
        s {str} -- string of last flattened category, used for 
            the detail page
        campus {list of dict} -- list of flattened campus information 
            to be fed into query builder
    """
    res, s, campus = [], '', []
    for cat in d.keys():
        for bucket in d[cat].keys():
            for choice in d[cat][bucket]:
                if cat != 'Campus':
                    res.append({cat: {bucket: choice}})
                else:
                    campus.append({bucket: choice})
                if output_str:
                    s = cat + ' - ' + bucket + ' - ' + d[cat][bucket]
    return res, s, campus


# build search query from json sent by front end
def build_query(raw_json):
    keywords = raw_json.pop('keywords', None)
    criteria, _, campus = unroll_cat(raw_json)
    query_list = []
    if keywords:
        query_list.append({"$text": {"$search": keywords}})
    if criteria: 
        query_list.append({"category": {'$in': criteria}})
    if campus: 
        query_list.append({'campus': {'$in': campus}})

    # use $and operator if more than 1 criteria
    if len(query_list)>1: 
        query = {'$and': query_list}
    elif len(query_list)==1: 
        query = query_list[0]
    else: query = {}

    return query


def get_equipments(list_of_ids):
    """
    Gets a list of documents (as cursor objects) given a list of ObjectID
    """
    inventory_collection = get_db()['inventory']
    equipments = list(inventory_collection.find({'_id': {'$in': list_of_ids}}))
    return equipments
     

def get_one_equipment(_id):
    """
    Gets 1 document (as cursor object) given an ObjectID
    """
    inventory_collection = get_db()['inventory']
    return inventory_collection.find_one({'_id': _id})


def update_one_equipment(_id, updates):
    """Update a document

    Arguments:
        _id {ObjectId} -- id of document to be updated
        updates {dict} -- update to be committed
    """
    inventory_collection = get_db()['inventory']
    update_result = inventory_collection.replace_one({'_id': _id},  updates)


def insert_one_equipment(insert):
    """Insert a document

    Arguments:
        insert {dict} -- document to be inserted   

    Returns:
        {ObjectId} -- id of inserted object
    """
    inventory_collection = get_db()['inventory']
    inserted_result = inventory_collection.insert_one(insert)
    return inserted_result.inserted_id
    


def get_user_by_username(username):
    """Get a user by username

    Arguments:
        username {str} -- user's username

    Returns:
        {dict or None} -- return None if username not found
    """
    user_collection = get_db()['user']
    user_list = list(user_collection.find({'username': username}))
    return user_list[0] if user_list != [] else None


