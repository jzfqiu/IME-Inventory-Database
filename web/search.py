"""search logic"""

import json
import math
import re
from hashlib import blake2b
from bson.objectid import ObjectId

from flask import Blueprint, render_template, request, session, current_app, redirect, url_for
from web import db
from web.utils import *


RESULT_PER_PAGE = 15
search_bp = Blueprint('search', __name__)


# search: return search page skeleton
# search.js: send request for result with empty criteria
# fetch: fetch results from db, return a populated html page
# search.js: async receive html and insert into search.html



@search_bp.route('/', methods=('GET', 'POST'))
def search():
    """
    Front page: render sidebar and top
    """
    with open('test_data/test_cats.json') as cats:
        cats_data = list(json.load(cats).values())
    return render_template('search.html',
                           cats=cats_data,
                           logged_in_user=get_logged_in_user())


@search_bp.route('/fetch/page/<page_number>', methods=['POST'])
def fetch_page(page_number):
    collection = db.get_db()['inventory']
    query = db.build_query(request.json)
    batch = collection.find(query).limit(
        RESULT_PER_PAGE).skip((int(page_number)-1)*RESULT_PER_PAGE)
    batch_cnt = collection.count_documents(query)
    return render_template('results.html',
                           data=batch,
                           page_cnt=batch_cnt,
                           pages=range(math.ceil(batch_cnt / RESULT_PER_PAGE)),
                           cur_page=int(page_number))



@search_bp.route('/equipment/<_id>')
def equipment(_id):
    equipment = db.get_one_equipment(ObjectId(_id))
    cat = " - ".join(equipment['category'])
    campus_str = " - ".join(equipment['campus'])
    cleaned_location = re.sub(r'[^A-Za-z0-9]+', '+', equipment['location'])
    return render_template('equipment.html',
                           equipment=equipment,
                           cat=cat,
                           campus=campus_str,
                           GOOGLE_MAP_API_KEY=current_app.config['GOOGLE_MAP_API_KEY'],
                           logged_in_user=get_logged_in_user(),
                           cleaned_location=cleaned_location 
                            if cleaned_location else "+".join(equipment['campus']))




@search_bp.route('/help')
def help():
    return render_template('help.html', logged_in_user=get_logged_in_user())


@search_bp.route('/developer')
def developer():
    return render_template('developer.html', logged_in_user=get_logged_in_user())



# TODO: color coding by campus
