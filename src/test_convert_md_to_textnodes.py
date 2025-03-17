import unittest
from convert_md_to_textnodes import *

class TestSplitNodesDelimiters(unittest.TestCase):
    def test_split_many_delimiter_pairs(self):
        old_nodes = [
            TextNode("a**b**c**d**e", text_type = TextType.TEXT),
            TextNode("hello**world**!", text_type = TextType.TEXT)
        ]
        res = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(res, [
            TextNode("a", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode("c", TextType.TEXT),
            TextNode("d", TextType.BOLD),
            TextNode("e", TextType.TEXT),
            TextNode("hello", TextType.TEXT),
            TextNode("world", TextType.BOLD),
            TextNode("!", TextType.TEXT)
        ])
        
    def test_no_old_nodes(self):
        res = split_nodes_delimiter([], ".", TextType.BOLD)
        self.assertEqual(res, [])
    
    def test_no_TextTypeTEXT(self):
        old_nodes = [TextNode("a", TextType.BOLD)]
        res = split_nodes_delimiter(old_nodes, ".", TextType.BOLD)
        self.assertEqual(res, old_nodes)
    
    def test_mismatching_delimiters(self):
        old_nodes = [TextNode("a.b.c.d", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, ".", TextType.ITALIC)
    
    def test_no_delimiters(self):
        old_nodes = [
            TextNode("abc", TextType.TEXT),
            TextNode("def", TextType.TEXT)
        ]
        res = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
        self.assertEqual(res, old_nodes)