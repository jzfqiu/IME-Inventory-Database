"""
All pymongo operations are LAZY
"""

from flask import current_app, g
import pymongo
from web.utils import *
from bson.objectid import ObjectId



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
        categories {list of list} -- list of flattened category information 
            to be fed into query builder
        s {str} -- string of last flattened category, used for 
            the detail page
        campus {list of dict} -- list of flattened campus information 
            to be fed into query builder
    """
    categories, s, campus = [], '', []
    for cat in d.keys():
        for bucket in d[cat].keys():
            for choice in d[cat][bucket]:
                if cat != 'Campus':
                    categories.append([cat, bucket, choice])
                else:
                    campus.append([bucket, choice])
                if output_str:
                    s = cat + ' - ' + bucket + ' - ' + d[cat][bucket]
    return categories, s, campus


# build search query from json sent by front end
def build_query(raw_json):
    keywords = raw_json.pop('keywords', None)
    categories, _, campus = unroll_cat(raw_json)
    query_list = []
    if keywords:
        query_list.append({"$text": {"$search": keywords}})
    if categories: 
        query_list.append({"category": {'$in': categories}})
    if campus: 
        query_list.append({'campus': {'$in': campus}})

    # use $and operator if more than 1 criteria
    if len(query_list)>1: 
        query = {'$and': query_list}
    elif len(query_list)==1: 
        query = query_list[0]
    else: query = {}

    return query


def get_categories():
    """ 
    get category information from database
    """
    categories_collection = get_db()['categories']
    categories = categories_collection.find({})[0]
    categories.pop("_id")
    return categories

        

def update_categories(new_category):
    """check if new equipment's category is included in the database, insert if not

    Args:
        new_category (list): category of new equipment in the form of [cat, bucket, item]
    """
    categories_collection = get_db()['categories']
    categories = categories_collection.find({})[0]
    category_id = categories.pop("_id")
    dprint(new_category)
    cat, bucket, item = new_category[0], new_category[1], new_category[2]
    if new_category[0] not in categories:
        # new category
        categories[cat] = {
            "description": "", 
            "children": {
                bucket: {"children": [item]}
            }
        } 
    elif bucket not in categories[cat]:
        # new bucket and item
        categories[cat]['children'][bucket] = {"children": [item]}
    elif item not in categories[cat][bucket]['children']:
        # new item
        categories[cat]['children'][bucket]['children'].append(item)
    else:
        # new_category already exist, no need to do anything
        return
    categories_collection.replace_one({'_id': category_id},  categories)
    





def get_equipments(list_of_ids):
    """
    Gets a list of documents (as cursor objects) given a list of str_id
    """
    inventory_collection = get_db()['inventory']
    list_of_ids = [ObjectId(_id) for _id in list_of_ids]
    if list_of_ids:
        equipments = list(inventory_collection.find({'_id': {'$in': list_of_ids}}))
    else:
        equipments = []
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
        _id {str} -- string id of document to be updated
        updates {dict} -- update to be committed
    """
    inventory_collection = get_db()['inventory']
    update_result = inventory_collection.replace_one({'_id': ObjectId(_id)},  updates)


def delete_one_equipment(_id):
    """delete 1 equipment

    Args:
        _id (str): id of object to be deleted
    """
    inventory_collection = get_db()['inventory']
    deleted_object = inventory_collection.remove({'_id': ObjectId(_id)})


def insert_one_equipment(insert):
    """Insert a document

    Arguments:
        insert {dict} -- document to be inserted   

    Returns:
        {str} -- id of inserted object
    """
    inventory_collection = get_db()['inventory']
    inserted_result = inventory_collection.insert_one(insert)
    return str(inserted_result.inserted_id)
    


def get_user_by_id(_id):
    """Get a user by id

    Arguments:
        _id {str} -- user's id

    Returns:
        {dict or None} -- return None if id not found
    """
    user_collection = get_db()['user']
    user_list = list(user_collection.find({'_id': ObjectId(_id)}))
    return user_list[0] if user_list != [] else None


def insert_new_user(user_info):
    """add a new user to the database (no validation done here)

    Args: 
        user info containing following fields:
            name (str): full name of the user
            email (str): unique identifier for the user, used for login
            affiliation (str): 
            title (str):
            password (str): hashed hex password
    Returns:
        string ObjectId of user entry in database

    """
    # TODO: add database insertion error handling
    user_collection = get_db()['user']
    user_id = user_collection.insert(user_info)
    return str(user_id)

def update_user(_id, updates):
    """Update a manager's information

    Arguments:
        _id {str} -- string id of document to be updated
        updates {dict} -- update to be committed
    """
    user_collection = get_db()['user']
    update_result = user_collection.replace_one({'_id': ObjectId(_id)},  updates)
    



