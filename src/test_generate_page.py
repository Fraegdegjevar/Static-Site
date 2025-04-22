import unittest
from generate_page import *

class TestExtractTitle(unittest.TestCase):
    def test_no_h1(self):
        markdown = """lots of shit
        more shit
        etc
        ## h2!
        """
        with self.assertRaises(Exception):
            extract_title(markdown)
    
    def test_extract_buried_header(self):
        markdown = """not line 1
## not line 2
# line 3"""
        self.assertEqual("line 3", extract_title(markdown))
    
    