from flask import Blueprint, render_template, request, current_app
from web import db
from bson.objectid import ObjectId

search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    keywords = ''
    collection = db.get_db()['inventory']
    index_type = 'all'

    if request.method == 'POST' and request.form['keywords']:

        index_type = request.form['type']

        # dropping old index and creating new one for each search
        # (mongodb allows only 1 text index per collection)
        collection.drop_index("text_index")

        # all possible options for index and weights
        text_indexes = dict(
            all=[("tags", "text"), ("name", "text"), ("overview", "text"), ("key_features", "text")],
            name=[("name", "text")],
            features=[("key_features", "text")],
            applications=[("key_applications", "text")],
            tags=[("tags", "text")]
        )
        text_index_weights = dict(
            all={"tags": 10, "name": 5},
            name={"name": 1},
            features={"features": 1},
            applications={"applications": 1},
            tags={"tags": 1},
        )
        collection.create_index(text_indexes[index_type],
                                weights=text_index_weights[index_type],
                                name="text_index")

        keywords = request.form['keywords']
        batch = collection.find({"$text": {"$search": keywords}})

    else:
        batch = collection.find(None)
    return render_template('search.html', results=batch, keywords=keywords, type=index_type)


@search_bp.route('/doc/<obj_id>')
def document(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    return render_template('document.html', result=item)


# mask full image url when serving
@search_bp.route('/doc/full_images/<image>')
def full_images(image):
    return current_app.send_static_file('user_uploads/full_images/'+image)


@search_bp.route('/about')
def about():
    return render_template('about.html')
