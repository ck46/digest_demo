import os
import openai

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

bp = Blueprint('summarize', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/summarize', methods=('POST', 'GET'))
def get_summarize():
    # use gpt-3 to get summary
    if request.method == 'POST':
        text = request.form['prompt']
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f'\"{text}\"\n\n\nSummarize the above text.'
        response = openai.Completion.create(
            engine="davinci-instruct-beta",
            prompt=prompt,
            temperature=0.92,
            max_tokens=150,
            top_p=1.0,
            frequency_penalty=0.4,
            presence_penalty=0.0,
            stop=["\"\"\""]
            )
        summary = response['choices'][0]['text']
        return render_template('index.html', summary=summary, text=text)
    else:
        return redirect(url_for('index'))