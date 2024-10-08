import unittest
from app import app  # Import the Flask app

class FlaskAPITestCase(unittest.TestCase):

    def setUp(self): # Special testcase method that is called before each test
        self.app = app.test_client()
        self.app.testing = True
    
    def testFile1(self):
        response = self.app.get('/generatepdf?number=1')
        self.assertEqual(response.status_code, 200)
    
    def testFile2(self):
        response = self.app.get('/generatepdf?number=2')
        self.assertEqual(response.status_code, 200)
    
    def testFile3(self):
        response = self.app.get('/generatepdf?number=6')
        self.assertEqual(response.status_code, 400)
    
    def testFile4(self):
        response = self.app.get('/generatepdf?number=-1')
        self.assertEqual(response.status_code, 400)
    

