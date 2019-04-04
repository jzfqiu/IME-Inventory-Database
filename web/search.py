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
        results.append(process_item(item, 5))

    return render_template('search.html', results=results)


@search_bp.route('/doc/<obj_id>')
def document(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    result = process_item(item)
    return render_template('document.html', result=result)


def process_item(item, n=None):
    """
    :param item: a document (dict) returned by find_one() or batch iteration
    :param n: number of entry needed in detailed ['data']
    :return: another dict with _id and name seperated from other data
    """
    try:
        object_id = item.pop('_id')
        name = item.pop('name')
        if n:
            data = list(item.items())[:n]
        else:
            data = list(item.items())
    except KeyError:
        raise
    return {'id': object_id, 'name': name, 'data': data}