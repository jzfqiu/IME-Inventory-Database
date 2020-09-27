"""
Functions related to editing and creating new equipments
"""


import json
import math
import re
from hashlib import blake2b

from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
from web import db
from web.utils import *
from bson.objectid import ObjectId




edit_bp = Blueprint('edit', __name__)

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
        dprint(new_equipment)
        # attach manager id to the equipment
        dprint(get_logged_in_user())
        new_equipment['user'] = ObjectId(get_logged_in_user()['_id'])
        _id = db.insert_one_equipment(new_equipment)

        # add new equipment to its manager's equipment list
        manager_id = get_logged_in_user()['_id']
        manager_data = db.get_user_by_id(manager_id)
        if manager_data['equipments'] is None:
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
    is_manager = get_logged_in_user() == str(equipment_requested['user'])
    cleaned_location = re.sub(r'[^A-Za-z0-9]+', '+', equipment_requested['location'])
    if request.method == 'GET':
        return render_template('edit.html',
                                equipment=equipment_requested,
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                cleaned_location=cleaned_location,
                                logged_in_user=get_logged_in_user())
    else:
        updated_data = clean_equipment_data(json.loads(request.json))
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


