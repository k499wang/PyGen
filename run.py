from app import app  
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 

pdfs_folder = os.path.join(base_dir, '/backend/pdfs')  


if __name__ == '__main__':
    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)
    
    app.run(debug=True)  # CHANGE LATER TO app.run(debug=False) FOR PRODUCTION