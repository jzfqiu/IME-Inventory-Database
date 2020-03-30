from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
import json
import math
from web import db
from bson.objectid import ObjectId
from hashlib import blake2b

RESULT_PER_PAGE = 15
search_bp = Blueprint('search', __name__)


# search: return search page skeleton
# search.js: send request for result with empty criteria
# fetch: fetch results from db, return a populated html page
# search.js: asyn receive html and insert into search.html


def dprint(s):
    print(s, flush=True)


def get_logged_in_user():
    return session.get('username', None)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    with open('test_data/test_cats.json') as cats:
        cats_data = list(json.load(cats).values())
    return render_template('search.html',
                           cats=cats_data,
                           logged_in_user=get_logged_in_user())


@search_bp.route('/fetch/page/<page_number>', methods=['POST'])
def fetch_page(page_number):
    collection = db.get_db()['inventory']
    query = db.build_query(request.get_json())
    batch = collection.find(query).limit(
        RESULT_PER_PAGE).skip((int(page_number)-1)*RESULT_PER_PAGE)
    batch_cnt = collection.count_documents(query)
    return render_template('results.html',
                           data=batch,
                           page_cnt=batch_cnt,
                           pages=range(math.ceil(batch_cnt / RESULT_PER_PAGE)),
                           cur_page=int(page_number))


@search_bp.route('/fetch/login', methods=['POST'])
def fetch_login():
    user = list(db.get_db()['user'].find({'email': request.form['email']}))[0]
    hashed_pwd = blake2b(str.encode(request.form['password']), digest_size=10)
    if user is not None and user['password']==hashed_pwd.hexdigest():
        session['username'] = [user['username'], user['name']]
        return json.dumps({'success': True})
    else:
        return json.dumps({'success': False})


@search_bp.route('/fetch/logout')
def fetch_logout():
    del session['username']
    return redirect(url_for('search.search'))


@search_bp.route('/user/<username>')
def user(username):
    user = db.get_user_by_username(username)
    if user is not None:
        for k in ['_id', 'password']:
            user.pop(k)
        user_equipments = db.get_equipments(user['equipments'])
        user_equipments = [{'name': e['name'], 'id': str(e['_id'])} for e in user_equipments]
        is_manager = get_logged_in_user() and user['username']==get_logged_in_user()[0]
        return render_template('user.html', 
                                user=user,
                                logged_in_user=get_logged_in_user(),
                                equipments=user_equipments,
                                is_manager=is_manager)
    return redirect(url_for('search.search'))
        


@search_bp.route('/equipment/<_id>')
def equipment(_id):
    equipment = db.get_one_equipment(ObjectId(_id))
    _, cat, _ = db.unroll_cat(equipment['category'], True)
    return render_template('equipment.html',
                           equipment=equipment,
                           cat=cat,
                           GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                           logged_in_user=get_logged_in_user())


@search_bp.route('/equipment/edit/<_id>')
def edit_equipment(_id):
    equipment = db.get_one_equipment(ObjectId(_id))
    is_manager = get_logged_in_user()==equipment['user']
    return render_template('edit.html',
                            equipment=equipment,
                            is_manager=is_manager,
                            logged_in_user=get_logged_in_user())
    

@search_bp.route('/about')
def about():
    return render_template('about.html', logged_in_user=get_logged_in_user())





# TODO: Add location information
# TODO: color coding by campus
