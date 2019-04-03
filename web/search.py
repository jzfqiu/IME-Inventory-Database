from flask import Blueprint, render_template, request, flash
from web.db import get_db, find_all

search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    collection = get_db()['inventory']

    results = find_all(collection)
    if not results:
        results = ['No matched result']
    if request.method == 'POST':
        keywords = request.form['keywords']

        if not keywords:
            flash('Keywords cannot be empty', 'error')
        else:
            query = {'$text': {'search': keywords}}
            results = find_all(collection, query)

    return render_template('search.html', results=results)

