from flask import Blueprint, render_template
import json

search_bp = Blueprint('search', __name__)


@search_bp.route('/', methods=('GET', 'POST'))
def search():
    with open('test_cats.json') as cats:
        cats_data = list(json.load(cats).values())
    with open('test_data_v2.json') as demos:
        demo_data = list(json.load(demos).values())[0]
    return render_template('search.html', cats=cats_data, demos=demo_data)

# Add location inforamtion

# color coding by campus
