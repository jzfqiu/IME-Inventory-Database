from flask import Blueprint, render_template, request, flash
from web import db
from bson.objectid import ObjectId


search_bp = Blueprint('search', __name__)


@search_bp.route('/', defaults={'page': 0})
@search_bp.route('/<page>', methods=('GET', 'POST'))
def search(page):
    results = []
    batch = None
    collection = db.get_db()['inventory']

    # skip results from previous pages
    # ffrom = int(page)*5

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
        results.append(db.process_item(item, 5))

    return render_template('search.html', results=results)


@search_bp.route('/doc/<obj_id>')
def document(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    result = db.process_item(item)
    return render_template('document.html', result=result)

