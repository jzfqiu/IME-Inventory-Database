from flask import Blueprint, render_template, request, url_for, redirect
from web import db
from bson.objectid import ObjectId

edit_bp = Blueprint('edit', __name__, url_prefix='/edit')


@edit_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        # add new document
        collection = db.get_db()['inventory']
        new_doc = {
            'name': request.form['name'],
            request.form['key1']: request.form['value1'],
            request.form['key2']: request.form['value2'],
            request.form['key3']: request.form['value3']
        }
        collection.insert_one(new_doc)
        return redirect(url_for('search.search'))
    else:
        # prepare empty fields
        return render_template('edit.html', obj_id='new')


@edit_bp.route('/<obj_id>', methods=['GET', 'POST'])
def edit(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    result = db.process_item(item)

    if request.method == 'POST':
        pass
    else:
        pass


