from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from digestai.utils import get_summary

bp = Blueprint('summarize', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/summarize', methods=('POST', 'GET'))
def get_summarize():
    # use gpt-3 to get summary
    if request.method == 'POST':
        text = request.form['prompt'] 
        summary = get_summary(text)
        return render_template('index.html', summary=summary, text=text)
    else:
        return redirect(url_for('index'))
