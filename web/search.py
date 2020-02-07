from flask import Blueprint, render_template, request, session, current_app
import json
import math
from web import db

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
                           cats=cats_data,
                           GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'])


@search_bp.route('/fetch/<page_number>', methods=['POST'])
def fetch(page_number):
    criteria = request.get_json()
    collection = db.get_db()['inventory']
    batch = collection.find(None).limit(RESULT_PER_PAGE).skip(
        (int(page_number)-1)*RESULT_PER_PAGE)
    batch_cnt = collection.count(None)
    return render_template('results.html',
                           data=batch,
                           page_cnt=batch_cnt,
                           pages=range(math.ceil(batch_cnt / RESULT_PER_PAGE)))





# TODO: Add location information
# TODO: color coding by campus
