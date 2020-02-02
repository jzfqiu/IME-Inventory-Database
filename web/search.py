from flask import Blueprint, render_template, request, session
import json
import math
from web import db

RESULT_PER_PAGE = 15
search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
@search_bp.route('/page/<page_number>', methods=('GET', 'POST'))
def search(page_number='1'):
    collection = db.get_db()['inventory']
    if request.method == 'POST' and request.form['keywords']:
        keywords = request.form['keywords']
        batch = collection.find({"$text": {"$search": keywords}})
        batch_cnt = collection.count({"$text": {"$search": keywords}})
    else:
        batch = collection.find(None).limit(RESULT_PER_PAGE).skip(
            (int(page_number)-1)*RESULT_PER_PAGE)
        batch_cnt = collection.count(None)
    with open('test_data/test_cats.json') as cats:
        cats_data = list(json.load(cats).values())
    return render_template('search.html',
                           cats=cats_data,
                           data=batch,
                           page_cnt=batch_cnt,
                           pages=range(math.ceil(batch_cnt/RESULT_PER_PAGE)))

# Add location information
# color coding by campus
