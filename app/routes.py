from app import app
from flask import Blueprint, send_file, request, jsonify, after_this_request, render_template
from backend.pdfHandle import pdfHandler
import os
import zipfile


base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) 
pdfs_folder = os.path.join(base_dir, 'pdfs')  
zip_name = "generated_pdfs.zip" 
zip_path = os.path.join(pdfs_folder, zip_name)  


main = Blueprint('main', __name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generatepdf', methods = ['GET'])
def generatepdf():
    try:
        num_pages = request.args.get('number', default=1, type=int)
            
        if num_pages <= 0 or num_pages >= 6:
            return jsonify({'error': 'Invalid number of pages. Must be a positive integer less than 6'}), 400

        generated_pdfs = pdfHandler(num_pages)
        if len(generated_pdfs) == 1:
            response = send_file(generated_pdfs[0], as_attachment=True)      
            return response
        elif len(generated_pdfs) > 1:
            zip_file = zip_pdfs(generated_pdfs)
            response = send_file(zip_file, as_attachment=True)
                        
            return response
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    if os.path.exists(zip_path):
        os.remove(zip_path)
        
    
    
def zip_pdfs(pdf_paths):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for pdf in pdf_paths:
            zipf.write(pdf, os.path.basename(pdf))  # Add PDF to the zip file
    return zip_path