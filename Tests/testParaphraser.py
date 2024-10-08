import unittest
from tools.paraphraser import paraphrase

class TestParaphraser(unittest.TestCase):
    
    def test_case_1(self):
        result = paraphrase("This is a test paragraph.")
        self.assertNotEqual(result, "This is a test paragraph.")
    