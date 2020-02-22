from flask import Blueprint, render_template, request, session, current_app
import json
import math
from web import db
from bson.objectid import ObjectId

RESULT_PER_PAGE = 15
search_bp = Blueprint('search', __name__)


# search: return search page skeleton
# search.js: send request for result with empty criteria
# fetch: fetch results from db, return a populated html page
# search.js: asyn receive html and insert into search.html


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    with open('test_data/test_cats.json') as cats:
        cats_data = list(json.load(cats).values())
    return render_template('search.html',
                           cats=cats_data)


@search_bp.route('/fetch/<page_number>', methods=['POST'])
def fetch(page_number):
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


@search_bp.route('/details/<_id>')
def details(_id):
    collection = db.get_db()['inventory']
    res = collection.find_one({'_id': ObjectId(_id)})
    _, cat, _ = db.unroll_cat(res['category'], True)
    return render_template('details.html',
                           result=res,
                           cat=cat,
                           GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'])


@search_bp.route('/about')
def about():
    return render_template('about.html')


@search_bp.route('/contact')
def contact():
    return render_template('contact.html')


@search_bp.route('/policy')
def policy():
    return render_template('policy.html')




# TODO: Add location information
# TODO: color coding by campus
