from flask import Blueprint, render_template, request, url_for, redirect
from web import db
from bson.objectid import ObjectId

edit_bp = Blueprint('edit', __name__, url_prefix='/edit')


@edit_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        collection = db.get_db()['inventory']
        new_doc = process_form(request.form)
        collection.insert_one(new_doc)
        return redirect(url_for('search.search'))
    else:
        return render_template('edit.html', obj_id='new', result=None)


@edit_bp.route('/<obj_id>', methods=['GET', 'POST'])
def edit(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    if request.method == 'POST':
        new_doc = process_form(request.form)
        collection.find_one_and_replace({'_id': ObjectId(obj_id)}, new_doc)
        return redirect(url_for('search.document', obj_id=obj_id))
    else:
        return render_template('edit.html', obj_id=obj_id, result=item)


@edit_bp.route('/del/<obj_id>')
def delete(obj_id):
    collection = db.get_db()['inventory']
    collection.delete_one({'_id': ObjectId(obj_id)})
    return redirect(url_for('search.search'))


def process_form(raw_form):
    new_doc = {
        'name': None,
        'overview': None,
        'key_applications': [],
        'key_features': [],
        'tags': []
    }
    for key in raw_form.keys():
        if key == 'name':
            new_doc['name'] = raw_form[key]
        elif key == 'overview':
            new_doc['overview'] = raw_form[key]
        elif 'feature' in key:
            new_doc['key_features'].append(raw_form[key])
        elif 'application' in key:
            new_doc['key_applications'].append(raw_form[key])
        elif 'tag' in key:
            new_doc['tags'].append(raw_form[key])
        elif key is 'documentation':
            new_doc['documentation'].append(raw_form[key])

    return new_doc
