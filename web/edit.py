from flask import Blueprint, render_template, request, url_for, redirect, current_app
from web import db
from bson.objectid import ObjectId
import os
import uuid
from PIL import Image

edit_bp = Blueprint('edit', __name__, url_prefix='/edit')

# TODO: move these global variables to configuration file
UPLOAD_ROOT = 'web/static/user_uploads'
FULL_IMAGE_PATH = os.path.join(UPLOAD_ROOT, 'full_images')
THUMBNAILS_PATH = os.path.join(UPLOAD_ROOT, 'thumbnails')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


@edit_bp.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        collection = db.get_db()['inventory']
        new_doc = process_form(request.form)
        process_image(request, new_doc)
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


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def process_form(raw_form):
    new_doc = {}
    for key in raw_form.keys():
        if key == 'name':
            new_doc['name'] = raw_form[key]
        elif key == 'overview':
            new_doc['overview'] = raw_form[key]
        elif 'feature' in key:
            create_or_append(new_doc, 'key_features', raw_form[key])
        elif 'application' in key:
            create_or_append(new_doc, 'key_applications', raw_form[key])
        elif 'tag' in key:
            create_or_append(new_doc, 'tags', raw_form[key])
        elif key is 'documentation':
            new_doc['documentation'] = raw_form[key]
    return new_doc


def process_image(req, new_doc):
    # if upload input is filled:
    if 'image' in req.files:
        file = req.files['image']
        # if file is real with allowed extension
        if file and allowed_file(file.filename):
            filename = uuid.uuid4().hex + '.' + file.filename.rsplit('.', 1)[1].lower()
            new_doc['image'] = filename
            # store full image
            full_image_path = os.path.join(FULL_IMAGE_PATH, filename)
            file.save(full_image_path)
            # store thumbnails
            thumbnail_path = os.path.join(THUMBNAILS_PATH, filename)
            im = Image.open(file)
            im.thumbnail((128, 128))
            im.save(thumbnail_path)


def create_or_append(d, key, val):
    try:
        d[key].append(val)
    except KeyError:
        d[key] = [val]
