from app import create_app
import os

base_dir = os.path.dirname(os.path.abspath(__file__)) 

pdfs_folder = os.path.join(base_dir, '/backend/pdfs')  


if __name__ == '__main__':
    if not os.path.exists(pdfs_folder):
        os.makedirs(pdfs_folder)
    
    app = create_app()  # Run the Flask app
    app.run(debug=True, host='0.0.0.0')  # Run the Flask app