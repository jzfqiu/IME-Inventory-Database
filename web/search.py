from flask import Blueprint, render_template, request
from web import db
from bson.objectid import ObjectId


search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    keywords = ''
    collection = db.get_db()['inventory']

    if request.method == 'POST' and request.form['keywords']:

        indexes = collection.index_information()
        if "default_index" not in indexes:
            text_index = [
                ("tags", "text"),
                ("name", "text"),
                ("overview", "text"),
                ("key_features", "text")
            ]
            text_index_weight = {
                "text": 10,
                "name": 5
            }
            collection.create_index(text_index, weights=text_index_weight, name="default_index")

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