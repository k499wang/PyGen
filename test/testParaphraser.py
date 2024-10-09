import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  
from tools.pdfGenerator import paraphrase

class TestParaphraser(unittest.TestCase):
    def test_case_1(self):
        result = paraphrase("This is a test paragraph.")
        self.assertNotEqual(result, "This is a test paragraph.")
    
    def test_case_2(self):
        result = paraphrase("")
        self.assertNotEqual(result, "")
    