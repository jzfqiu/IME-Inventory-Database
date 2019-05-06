from flask import Blueprint, render_template, request
from web import db
from bson.objectid import ObjectId


search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    keywords = ''
    collection = db.get_db()['inventory']

    if request.method == 'POST' and request.form['keywords']:
        text_index = [("name", "text"),
                      ("overview", "text"),
                      ("key_features", "text")]
        collection.create_index(text_index)
        keywords = request.form['keywords']
        batch = collection.find({"$text": {"$search": keywords}})

    else:
        batch = collection.find(None)
    return render_template('search.html', results=batch, keywords=keywords)


@search_bp.route('/doc/<obj_id>')
def document(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    return render_template('document.html', result=item)


@search_bp.route('/about')
def about():
    return render_template('about.html')