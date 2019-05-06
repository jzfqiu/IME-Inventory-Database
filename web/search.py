from flask import Blueprint, render_template, request
from web import db
from bson.objectid import ObjectId


search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    results = []
    keywords = ''
    collection = db.get_db()['inventory']

    if request.method == 'POST' and request.form['keywords']:
        # This search method queries everything into server and process using
        # backend script. It is ok with the amount of data we will need to
        # handle but will be very resource consume for larger database.
        # Consider implementing mongodb's text index search if possible.
        collection.create_index({"$**": "text"})
        batch = [None]
        keywords = request.form['keywords']
        for item in batch:
            if keywords in item.keys() or keywords in item.values():
                results.append(db.process_item(item, 5))
    else:
        batch = collection.find(None)
        # for item in batch:
        #     results.append(db.process_item(item, 5))

    return render_template('search.html', results=batch, keywords=keywords)


@search_bp.route('/doc/<obj_id>')
def document(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    # result = db.process_item(item)
    return render_template('document.html', result=item)


@search_bp.route('/about')
def about():
    return render_template('about.html')