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
    
    def test_empty_string(self):
        md = """
        
        """
        self.assertListEqual(
           [], markdown_to_blocks(md)
           )
        
    def test_one_block(self):
        md = "All text is in one block!"
        expected_blocks = ["All text is in one block!"]
        self.assertListEqual(expected_blocks, markdown_to_blocks(md))
    
class TestBlockToBlockType(unittest.TestCase):
    def test_empty_string(self):
        block = ""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))
    
    def test_basic_string(self):
        block = "just text and nothing else"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))
    
    def test_heading(self):
        block = "### this is a heading"
        self.assertEqual(BlockType.HEADING, block_to_blocktype(block))
 
    def test_wrong_heading_no_space(self):
        block = "###this is a heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))
     
    def test_wrong_heading_hashes(self):
        block = "####### this is a heading"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))    

    def test_code(self):
        block = "``` this is a heading```"
        self.assertEqual(BlockType.CODE, block_to_blocktype(block))

    def test_mismatched_code(self):
        block = "``` this is a heading``"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))
    
    def test_quote(self):
        block = ">this is a heading"
        self.assertEqual(BlockType.QUOTE, block_to_blocktype(block))
    
    def test_ord_list(self):
        block = """1. this
2. is
3. ordered"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(block))
    
    def test_wrong_number_ord_list(self):
        block = """1. this
4. isn't
3. ordered!"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))

    def test_wrong_format_ord_list(self):
        block = """1. this
2. is
3.ordered
4. but missing a space after 3.!"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))

    def test_unord_list(self):
        block = """- this
- is
- unordered!"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(block))

    def test_wrong_format_unord_list(self):
        block = """- this
-is
- unordered!
-but lacks spaces after -!"""
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(block))

    
    
    