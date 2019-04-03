from flask import Blueprint, render_template, request, flash
from web.db import get_db


search_bp = Blueprint('search', __name__)


@search_bp.route('/', defaults={'page': 0})
@search_bp.route('/<page>', methods=('GET', 'POST'))
def search(page):
    results = []
    batch = None
    collection = get_db()['inventory']

    # skip results from previous pages
    ffrom = int(page)*5

    if request.method == 'POST':
        keywords = request.form['keywords']

        if not keywords:
            flash('Keywords cannot be empty', 'error')
        else:
            query = {'$text': {'$search': keywords}}
            batch = list(collection.find(query))
    else:
        batch = collection.find(None)

    for item in batch:
        object_id = item.pop('_id')

        results.append({'id': object_id, 'data': item})

    return render_template('search.html', results=results)

