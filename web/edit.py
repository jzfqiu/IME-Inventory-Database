"""
Functions related to editing and creating new equipments
"""


import json
import math
import re
from hashlib import blake2b

from flask import Blueprint, render_template, request, session, current_app, redirect, url_for, abort
from web import db
from web.utils import *
from bson.objectid import ObjectId




edit_bp = Blueprint('edit', __name__)


def clean_equipment_data(data):
    """
    Clean data sent from edit form into database object

    Specifically, convert flattened category list to dict 
    and encapsulate contact information
    """
    if 'features' in data:
        data['features'] = [f for f in data['features'] if f != ""]
    if 'applications' in data:
        data['applications'] = [a for a in data['applications'] if a != ""]
    data['category'] = [
        data.pop('cat'), 
        data.pop('bucket'), 
        data.pop('item')
    ]
    data['campus'] = [data.pop('campus'), data.pop('department')]
    data['contact'] = {
        "name": data.pop('contact-name'),
        "title": data.pop('contact-title'),
        "email": data.pop('contact-email'),
        "tel": data.pop('contact-tel')
    }
    if data['location'] == "":
        data['location'] = ",".join(data['campus'])
    
    return data

@edit_bp.route('/equipment/edit/new', methods=['POST', 'GET'])
def new_equipment():
    if request.method == 'GET':
        return render_template('edit.html',
                                equipment={},
                                cleaned_location="united+states",
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                logged_in_user=get_logged_in_user())
    else:
        new_equipment = clean_equipment_data(json.loads(request.json))
        
        # attach manager id to the equipment
        new_equipment['user'] = ObjectId(get_logged_in_user()['_id'])
        _id = db.insert_one_equipment(new_equipment)

        # add new equipment to its manager's equipment list
        manager_id = get_logged_in_user()['_id']
        manager_data = db.get_user_by_id(manager_id)
        if "equipments" not in manager_data or manager_data['equipments'] is None:
            manager_data['equipments'] = [_id]
        else:
            manager_data['equipments'].append(_id)

        # insert new category if not present in the database
        db.update_categories(new_equipment['category'])

        # also update the manager's list of managed equipments
        db.update_user(manager_id, manager_data)

        return json.dumps({
            "success": True,
            "return_url": "/equipment/"+str(_id)
        })


@edit_bp.route('/equipment/edit/<_id>', methods=['POST', 'GET'])
def edit_equipment(_id):
    equipment_requested = db.get_one_equipment(_id)
    if not get_logged_in_user() or get_logged_in_user()['_id'] != str(equipment_requested['user']):
        # no user logged in or user not managing the equipment
        abort(403, description="You are not logged in as the manager of this equipment")
    cleaned_location = re.sub(r'[^A-Za-z0-9]+', '+', equipment_requested['location'])
    if request.method == 'GET':
        return render_template('edit.html',
                                equipment=equipment_requested,
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                cleaned_location=cleaned_location,
                                logged_in_user=get_logged_in_user())
    else:
        updated_data = clean_equipment_data(json.loads(request.json))
        # attach manager id to the equipment
        updated_data['user'] = ObjectId(get_logged_in_user()['_id'])
        db.update_one_equipment(_id, updated_data)
        return json.dumps({
            "success": True,
            "return_url": "/equipment/"+str(_id)
        })
        


@edit_bp.route('/fetch/edit/categories', methods=['GET'])
def fetch_cat():
    categories = db.get_categories()
    return json.dumps(categories)


@edit_bp.route('/equipment/delete/<_id>', methods=['GET'])
def delete_equipment(_id):
    db.delete_one_equipment(_id)
    # also update manager's equipment data
    manager_id = get_logged_in_user()['_id']
    manager_data = db.get_user_by_id(manager_id)
    manager_data['equipments'].remove(_id)
    db.update_user(manager_id, manager_data)
    return redirect(url_for('user.user', _id=manager_id))


