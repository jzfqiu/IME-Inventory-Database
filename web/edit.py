"""
Functions related to editing and creating new equipments
"""


import json
import math
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
    existing_cat = flatten_dict(equipment_requested['category'])
    if request.method == 'GET':
        return render_template('edit.html',
                                equipment=equipment_requested,
                                existing_cat=existing_cat,
                                is_manager=is_manager,
                                GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                                logged_in_user=get_logged_in_user())
    else:
        updated_data = clean_update_data(json.loads(request.json))
        db.update_one_equipment(_id, updated_data)
        return json.dumps({"success": True})
        


@edit_bp.route('/fetch/edit/cat', methods=['POST'])
def fetch_cat():
    with open('test_data/test_cats_v2.json') as cats:
        cats_data = json.load(cats)
    data = request.json
    cat = data.get('cat', None)
    bucket = data.get('bucket', None)
    if bucket is None:
        return json.dumps(list(cats_data[cat].keys()))
    return json.dumps(cats_data[cat][bucket])