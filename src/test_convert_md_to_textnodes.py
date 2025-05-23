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
        
class TestTextToTextNodes(unittest.TestCase):
    def test_all_md_types_in_string(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                ]
        self.assertListEqual(expected_nodes, text_nodes)
    
    def test_empty_string_returns_empty_string(self):
        text = ""
        text_nodes = text_to_textnodes(text)
        self.assertListEqual([], text_nodes)
    
    def test_string_no_markdown(self):
        text = "Just a normal string with no markdown!"
        text_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], text_nodes)
    
    def test_mistmatching_delimiters(self):
        text = "Odd **number* of delimiters!"
        with self.assertRaisesRegex(Exception,"Invalid Markdown! Mismatching delimiters. Did you forget a closing delimiter?"):
            text_to_textnodes(text)
    
    def test_misplaced_delimiters_mismatch(self):
        text = "**Delims are *misplaced* and should mismatch!"
        with self.assertRaisesRegex(Exception,"Invalid Markdown! Mismatching delimiters. Did you forget a closing delimiter?"):
            text_to_textnodes(text)
            
    def test_repeated_md_type(self):
        text = "_italic here_ and _italic again_ and then _the final italic_"
        text_nodes = text_to_textnodes(text)
        expected_nodes = [
            TextNode("italic here", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic again", TextType.ITALIC),
            TextNode(" and then ", TextType.TEXT),
            TextNode("the final italic", TextType.ITALIC)
            ]
        self.assertListEqual(expected_nodes,
                             text_nodes)
    
    def test_image_at_start_of_string(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) at start of string!"
        text_nodes = text_to_textnodes(text)
        expected_notes = [
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" at start of string!", TextType.TEXT)
        ]
        self.assertListEqual(expected_notes, text_nodes)
        