""" user routing and logic """
# user login/logout
# user registration
# user detail page


import json
import math
import re
from hashlib import blake2b
from bson.objectid import ObjectId

from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
from web import db
from web.utils import *

user_bp = Blueprint('user', __name__)


@user_bp.route('/register', methods=['GET'])
def get_register():
    """display user registration page

    Returns:
        template render
    """
    return render_template('register.html', logged_in_user=get_logged_in_user())


@user_bp.route('/register', methods=['POST'])
def post_register():
    """process user registration form information. logs user in if successful

    Returns:
        json: success status and error message if failed
    """
    # check if user with this email already exist
    # TODO: change error message after adding password retrieval function
    user_requested = list(db.get_db()['user'].find({'email': request.form['email']}))
    if user_requested:
        return json.dumps({'success': False, 'message': "User already exist. Please contact site manager for password reset."})
    
    # check access code
    if current_app.config['ACCESS_CODE'] != request.form['access-code']:
        return json.dumps({'success': False, 'message': "Wrong access code. Please try again."})
    
    hashed_pwd = blake2b(str.encode(request.form['password']), digest_size=10)
    new_user_info = {
        "name": request.form['full-name'],
        "email": request.form['email'],
        "password": hashed_pwd.hexdigest(),
        "affiliation": request.form['affiliation'],
        "title": request.form['title']
    }
    new_user_id = db.insert_new_user(new_user_info)

    return json.dumps({'success': True})


@user_bp.route('/fetch/login', methods=['POST'])
def fetch_login():
    user_requested = list(db.get_db()['user'].find({'email': request.form['email']}))[0]
    hashed_pwd = blake2b(str.encode(request.form['password']), digest_size=10)
    if user_requested is not None and user_requested['password']==hashed_pwd.hexdigest():
        session['logged_in_user'] = {
            '_id': str(user_requested['_id']), 
            'name': user_requested['name'], 
            'email': user_requested['email']
        }
        return json.dumps({'success': True})
    return json.dumps({'success': False})



@user_bp.route('/fetch/logout')
def fetch_logout():
    del session['logged_in_user']
    return redirect(url_for('search.search'))


@user_bp.route('/user/<_id>')
def user(_id):
    user_requested = db.get_user_by_id(ObjectId(_id))
    if user_requested is not None:
        user_requested.pop("password")
        if "equipments" in user_requested:
            user_equipments = db.get_equipments(user_requested['equipments'])
            user_equipments = [{'name': e['name'], 'id': str(e['_id'])} for e in user_equipments]
        else:
            user_equipments = None
        is_manager = get_logged_in_user() and str(user_requested['_id']) == get_logged_in_user()['_id']
        return render_template('user.html',
                                user=user_requested,
                                logged_in_user=get_logged_in_user(),
                                equipments=user_equipments,
                                is_manager=is_manager)
    return redirect(url_for('search.search'))