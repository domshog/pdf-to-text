from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os

import pytesseract
from PIL import Image
from pdf2image import convert_from_path

app = Flask(__name__)

# Path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            text_output = extract_text(file_path)
            return render_template('result.html', text_output=text_output)
    return redirect(request.url)


def extract_text(pdf_file):
    pages = convert_from_path(pdf_file, 300)
    text_output = []
    for page in pages:
        text = pytesseract.image_to_string(page, lang='eng')
        text_output.append(text)
    full_text = '\n'.join(text_output)
    return full_text


if __name__ == '__main__':
    app.run(debug=False)

