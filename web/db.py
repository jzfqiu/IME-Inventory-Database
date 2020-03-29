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
        res {list of dict} -- list of flattened category information to be fed into query builder
        s {str} -- string of last flattened category, used for the detail page
        campus {list of dict} -- list of flattened campus information to be fed into query builder
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