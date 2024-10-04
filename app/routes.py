from flask import send_file, request, render_template
from backend.pdfHandle import pdfHandler

import os

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate-pdf')
def generate_pdf_route():
    pdfHandler
    return send_file(pdf_path, as_attachment=True)