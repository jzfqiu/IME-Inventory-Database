from flask import Blueprint, g, render_template, request, session, url_for, redirect
from web.db import get_db, insert_many

edit_bp = Blueprint('edit', __name__)


@edit_bp.route('/new', methods=['GET', 'POST'])
def edit():
    if request.method == 'POST':
        collection = get_db()['inventory']
        new_doc = {
            request.form['key1']: request.form['value1'],
            request.form['key2']: request.form['value2'],
            request.form['key3']: request.form['value3']
        }
        insert_many(collection, new_doc)
        return redirect(url_for('search'))
    else:
        return render_template('edit.html')

