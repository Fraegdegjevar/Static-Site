import unittest
from block_markdown import *

class TestMarkDownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
         md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""" 
         blocks = markdown_to_blocks(md)
         expected_blocks = [
             "This is **bolded** paragraph",
             "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
             "- This is a list\n- with items"
             ]
         self.assertListEqual(expected_blocks, blocks)
         
    def test_leading_trailing_whitespace(self):
        md = """
    First line with whitespace

        more whitespace for second paragraph
"""
        blocks = markdown_to_blocks(md)
        expected_blocks = [
            "First line with whitespace",
            "more whitespace for second paragraph"
        ]
        self.assertListEqual(expected_blocks, blocks)
    
                