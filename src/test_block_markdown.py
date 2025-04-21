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

class TestBlockTextToChildren(unittest.TestCase):
    def test_block_text_ignore_markdown(self):
        text= "**ignore bold** text and this should _not_ be italic"
        expected_nodes = [LeafNode(None, "**ignore bold** text and this should _not_ be italic")]
        self.assertListEqual(expected_nodes, block_text_to_children(text, True))
    
    def test_block_text_markdown(self):
        text = "**bold text** text and this should _be italic_ and ooh an ![image text](https://www.google.co.uk) image"
        expected_nodes = [
            LeafNode("b", "bold text"),
            LeafNode(None, " text and this should "),
            LeafNode("i", "be italic"),
            LeafNode(None, " and ooh an "),
            LeafNode("img", "", props = {"src": "https://www.google.co.uk", "alt": "image text"}),
            LeafNode(None, " image")
            ]
        self.assertListEqual(expected_nodes, block_text_to_children(text))
        
    def test_empty_block(self):
        text = ""
        expected_nodes = []
        self.assertListEqual(expected_nodes, block_text_to_children(text))
        
    def test_wrap_nodes(self):
        block = """**Bold first item**
_italic second item_
normal third item"""
        expected_nodes = [
            ParentNode("li", [LeafNode("b", "Bold first item")]),
            ParentNode("li", [LeafNode("i", "italic second item")]),
            ParentNode("li", [LeafNode(None, "normal third item")])
            ]
        self.assertListEqual(expected_nodes, block_text_to_children(block, False, "li"))
        

class TestBlockToHtmlNode(unittest.TestCase):
    def test_quote_block_with_md(self):
        block = """>**quote1 bold** q1 not bold
>_quote2 italic_ q2 not italic
>`quote3 code` q3 not code"""
        expected_children = [
            LeafNode("b", "quote1 bold"),
            LeafNode(None, " q1 not bold"),
            LeafNode("i", "quote2 italic"),
            LeafNode(None, " q2 not italic"),
            LeafNode("code", "quote3 code"),
            LeafNode(None, " q3 not code")
        ]
        expected_node = ParentNode(tag="blockquote", children = expected_children)
        self.assertEqual(expected_node, block_to_html_node(block))
    
    def test_paragraph_with_md(self):
        block = """This is **just** a basic paragraph."""
        expected_children = [
            LeafNode(None, "This is "),
            LeafNode("b", "just"),
            LeafNode(None, " a basic paragraph.")
        ]
        expected_node = ParentNode("p", expected_children)
        self.assertEqual(expected_node, block_to_html_node(block))
    
    def test_ord_list_with_md(self):
        block = """1. **First bold** first not bold
2. _Second italic_ second not italic"""
        expected_children = [
            ParentNode("li", [LeafNode("b", "First bold"), LeafNode(None, " first not bold")]),
            ParentNode("li", [LeafNode("i", "Second italic"), LeafNode(None, " second not italic")])
        ]
        expected_node = ParentNode("ol", expected_children)
        self.assertEqual(expected_node, block_to_html_node(block))

        
    

    