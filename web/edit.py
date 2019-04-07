from flask import Blueprint, render_template, request, url_for, redirect
from web import db
from bson.objectid import ObjectId

edit_bp = Blueprint('edit', __name__, url_prefix='/edit')


@edit_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        collection = db.get_db()['inventory']
        new_doc = {'name': request.form['name']}
        for key in request.form.keys():
            if 'key' in key:
                new_doc[request.form[key]] = request.form['value'+key[-1]]

        collection.insert_one(new_doc)
        return redirect(url_for('search.search'))
    else:
        return render_template('edit.html', obj_id='new', result=None)


@edit_bp.route('/<obj_id>', methods=['GET', 'POST'])
def edit(obj_id):
    collection = db.get_db()['inventory']
    item = collection.find_one({'_id': ObjectId(obj_id)})
    result = db.process_item(item)

    if request.method == 'POST':
        new_doc = {'name': request.form['name']}
        for key in request.form.keys():
            if 'key' in key:
                new_doc[request.form[key]] = request.form['value'+key[-1]]
        collection.find_one_and_replace({'_id': ObjectId(obj_id)}, new_doc)
        return redirect(url_for('search.document', obj_id=obj_id))
    else:
        return render_template('edit.html', obj_id=obj_id, result=result)


@edit_bp.route('/del/<obj_id>')
def delete(obj_id):
    collection = db.get_db()['inventory']
    collection.delete_one({'_id': ObjectId(obj_id)})
    return redirect(url_for('search.search'))


