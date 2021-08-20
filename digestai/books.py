import os
import fitz
import json
import datetime
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_from_directory
)
from werkzeug.utils import secure_filename
from werkzeug.exceptions import abort
from os.path import join, dirname, realpath

from digestai.db import get_db
from digestai.utils import allowed_file

UPLOADS_PATH = join(dirname(realpath(__file__)), 'uploads')

# UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'PDF'}

bp = Blueprint('books', __name__)

@bp.route('/upload', methods=['GET', 'POST'])
def upload_file():
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
                'INSERT INTO upload (created_at, filename, filepath) VALUES (?, ?, ?)',
                (datetime.datetime.now(), filename, os.path.join(UPLOADS_PATH, filename))
            )
            db.commit()
            # process the file then add to mongodb
            return redirect(url_for('books.book_list'))
    return render_template('upload.html')


@bp.route('/books')
def book_list():
    db = get_db()
    uploads = db.execute(
        'SELECT * FROM upload ORDER BY created_at DESC'
    ).fetchall()
    print(uploads)
    return render_template('books.html', uploads=uploads)

@bp.route('/book/<id>')
def book_view(id):
    print(f"Download file requested: {id}")
    book_obj = get_upload(id)
    # book = book_obj['filepath']
    book = get_book_content(book_obj['filepath'])
    book_json_object = json.dumps(book)
    q = request.args.get('q')
    if q is not None:
        try:
            content = book[int(q)]
        except:
            content = None
    else:
        content = None
    return render_template('book.html', book=book, bookname=book_obj['filename'], book_id=id, content=content)

def get_upload(id):
    upload = get_db().execute(
        'SELECT id, filepath, filename'
        ' FROM upload'
        ' WHERE id = ?', id).fetchone()
    if upload is None:
        abort(404, f"Upload id {id} doesn't exist.")
    return upload

def get_book_content(book):
    doc = fitz.open(book)
    doc_toc = doc.get_toc()
    parent = None
    toc = dict()
    prev = None
    for i, c in enumerate(doc_toc):
        content = dict()
        content['level'] = int(c[0])
        content['title'] = c[1]
        content['page'] = c[2]
        content['children'] = dict()
        if parent is not None:
            if parent['level'] < content['level']:
                parent['children'][i] = content
            else:
                toc[i] = content
                parent = toc[i]
        else:
            toc[i] = content
            parent = toc[i]
        if prev is not None:
            prev['end_page'] = content['page']
            prev['raw_text'] = ''.join([doc[pn].getText() for pn in range(prev['page']-1, prev['end_page']-1)])
        if i == len(doc_toc)-1:
            content['end_page'] = doc.page_count
            content['raw_text'] = ''.join([doc[pn].getText() for pn in range(content['page']-1, content['end_page']-1)])
        prev = content
    return toc
