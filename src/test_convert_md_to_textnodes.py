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

class TestExtractMarkdownImages(unittest.TestCase):
    def test_many_matches(self):
        string = "there are several ![image_alt1](url1.co.uk) images here ![image_alt2](url2.co.uk)"
        res = extract_markdown_images(string)
        self.assertEqual(res, [
            ("image_alt1", "url1.co.uk"), 
            ("image_alt2", "url2.co.uk")
            ])
    def test_no_matches(self):
        string = "abc"
        res = extract_markdown_images(string)
        self.assertEqual(res, [])
        
    def test_empty_string(self):
        string = ""
        res = extract_markdown_images(string)
        self.assertEqual(res, [])

class TestExtractMarkdownLinks(unittest.TestCase):
    def test_many_matches(self):
        string = "there are many [anchor1](url1.co.uk) clickable urls [anchor2](url2.co.uk) in this string"
        res = extract_markdown_links(string)
        self.assertEqual(res, [
            ("anchor1", "url1.co.uk"), 
            ("anchor2", "url2.co.uk")
        ])
    
    def test_no_matches(self):
        string = "abc"
        res = extract_markdown_links(string)
        self.assertEqual(res, [])
    
    def test_empty_string(self):
        string = ""
        res = extract_markdown_images(string)
        self.assertEqual(res, [])

class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_no_images(self):
        node = TextNode("No images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("No images", TextType.TEXT)], new_nodes)
    
    def test_split_images_empty_list(self):
        node = []
        new_nodes = split_nodes_image(node)
        self.assertListEqual([], new_nodes)

class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes
        )
    def test_split_links_no_links(self):
        node = TextNode("No links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([TextNode("No links", TextType.TEXT)],
                             new_nodes)
    
    def test_split_links_empty_list(self):
        node = []
        new_nodes = split_nodes_link(node)
        self.assertListEqual([], new_nodes)
        