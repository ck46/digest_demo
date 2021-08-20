import os
import cv2
import pytesseract
import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from os.path import join, dirname, realpath

from digestai.utils import get_summary, allowed_file
from digestai.db import get_db

bp = Blueprint('images', __name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

def get_text_from_image(image_path):
    img = cv2.imread(image_path)
    # img = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    return pytesseract.image_to_string(img)

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static/image_uploads')

# UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'png', 'PNG', 'jpg', 'jpeg', 'JPG', 'JPEG'}
# image upload
@bp.route('/image/upload', methods=('POST', 'GET'))
def upload_image():
    if request.method == 'POST':
        db = get_db()
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOADS_PATH, filename))
            # need to save details to database before return from here
            db.execute(
                'INSERT INTO imageupload (created_at, filename, filepath) VALUES (?, ?, ?)',
                (datetime.datetime.now(), filename, os.path.join(UPLOADS_PATH, filename))
            )
            db.commit()
            # process the file then add to mongodb
            return redirect(url_for('images.image_list'))
    return render_template('image_upload.html')

@bp.route('/images')
def image_list():
    db = get_db()
    uploads = db.execute(
        'SELECT * FROM imageupload ORDER BY created_at DESC'
    ).fetchall()
    print(uploads)
    return render_template('images.html', uploads=uploads)

def get_upload(id):
    upload = get_db().execute(
        'SELECT id, filepath, filename'
        ' FROM imageupload'
        ' WHERE id = ?', id).fetchone()
    if upload is None:
        abort(404, f"Upload id {id} doesn't exist.")
    return upload

@bp.route('/image/<id>')
def image_text(id):
    print(f"Download file requested: {id}")
    image_obj = get_upload(id)
    # check if image_obj is actually of type image using upload type
    image_text = get_text_from_image(image_obj['filepath'])
    # check if summary parameter is provided
    q = request.args.get('q')
    if q is not None and q == 'summary':
        summary = get_summary(image_text)
        summarized = True
    else:
        summary = None
        summarized = False
    return render_template('image_content.html', image_name=image_obj['filename'], image_text=image_text, summary=summary, summarized=summarized)
