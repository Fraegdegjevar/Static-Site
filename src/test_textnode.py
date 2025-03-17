import unittest

from textnode import *

#instantiate two textnodes, use the assert equal method of the test case class
# on the two nodes to check that they are equal.
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_eq2(self):
        node = TextNode("these should be equal", TextType.TEXT, url="google.com")
        node2 = TextNode("these should be equal", TextType.TEXT, url="google.com")
        self.assertEqual(node, node2)
        
    def test_not_eq(self):
        node = TextNode("consider", TextType.ITALIC)
        node2 = TextNode("this", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = TextNode("same text", TextType.ITALIC)
        node2 = TextNode("same text", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_not_eq3(self):
        node = TextNode("same", TextType.CODE, url = "hello.com")
        node2 = TextNode("same", TextType.CODE, url = "google.com")
        self.assertNotEqual(node, node2)
    
    def test_not_eq4(self):
        node = TextNode("same", TextType.IMAGE, url = "hello.com")
        node2 = TextNode("same", TextType.IMAGE)
        self.assertNotEqual(node, node2)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_link(self):
        node = TextNode("a link", TextType.LINK, "will.co.uk")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "a link")
        self.assertEqual(html_node.props, {'href': "will.co.uk"})
    
    def test_image(self):
        node = TextNode("a nice image", TextType.IMAGE, url = "will.co.uk/image.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, 'img')
        self.assertEqual(html.value, '')
        self.assertEqual(html.props, {"src": "will.co.uk/image.png", "alt": "a nice image"})
            
if __name__ == "__main__":
    unittest.main()
