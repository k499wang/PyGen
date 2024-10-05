from app import app
from flask import Blueprint, send_file, request, render_template
from backend.pdfHandle import pdfHandler
import os

main = Blueprint('main', __name__)

@app.route('/api/generatepdf', methods = ['GET'])
def generatepdf():
    path = pdfHandler()
    return send_file(path, as_attachment=True)