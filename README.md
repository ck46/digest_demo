# Text Summarization using GPT-3
Digest demo is a flask app that implements the text summarization using GPT-3.

## Requiments
1. Python 3.6+
2. Tesseract-OCR

An executable instance of tesseract-ocr is required and the path to the executable will need to be specified in the `digestai/images.py` file in line `17` (this will be moved to a config file later).

## Installation
1. Clone the repo
2. CD into directory
3. Create a python virtual environment using the venv module and activate it.
4. Install requirements using pip
5. Set OpenAI API Key to the system environment variable "OPENAI_API_KEY"
6. Set FLASK_APP variable to 'digestai'
7. Set FLASK_ENV variable to development
8. Finally flask app with flask run command




