"""
Functions related to editing and creating new equipments
"""


import json
import math
import re
from hashlib import blake2b
from bson.objectid import ObjectId

from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
from web import db
from web.utils import *




edit_bp = Blueprint('edit', __name__)



@edit_bp.route('/equipment/edit/<_id>', methods=['POST', 'GET'])
def edit_equipment(_id):
    equipment_requested = db.get_one_equipment(ObjectId(_id))
    is_manager = get_logged_in_user() == equipment_requested['user']
    if request.method == 'GET':
        cleaned_location = re.sub(r'[^A-Za-z0-9]+', '+', equipment_requested['location'])
        return render_template('edit.html',
                                equipment=equipment_requested,
                                is_manager=is_manager,
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                cleaned_location=cleaned_location,
                                logged_in_user=get_logged_in_user())
    else:
        updated_data = clean_update_data(json.loads(request.json))
        dprint(updated_data)
        db.update_one_equipment(ObjectId(_id), updated_data)
        return json.dumps({
            "success": True,
            "return_url": "/equipment/"+str(_id)
        })
        


@edit_bp.route('/fetch/edit/cat', methods=['GET'])
def fetch_cat():
    with open('test_data/test_cats_v2.json') as cats:
        cats_dict = json.load(cats)
    return json.dumps(cats_dict)



@edit_bp.route('/equipment/edit/new', methods=['POST', 'GET'])
def new_equipment():
    if request.method == 'GET':
        return render_template('edit.html',
                                equipment={},
                                existing_cat=None,
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                logged_in_user=get_logged_in_user())
    else:
        return json.dumps({"success": True})