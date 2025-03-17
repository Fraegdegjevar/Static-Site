import unittest
from leafnode import LeafNode

class TestLeadNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "click", {"href": "googl.e"})
        node2 = LeafNode("a", "click", {"href": "googl.e"})
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = LeafNode("a", "click", {"href": "googl.e"})
        node2 = LeafNode("a", "click", {"hlef": "googl.e"})
        self.assertNotEqual(node, node2)
    
    def test_to_html(self):
        node = LeafNode("p", "Welcome!")
        self.assertEqual(node.to_html(), "<p>Welcome!</p>")
    
    def test_to_html2(self):
        node = LeafNode(value = "No tags!")
        self.assertEqual(node.to_html(), "No tags!")
    
    def test_to_html_no_value(self):
        node = LeafNode("p")
        with self.assertRaises(ValueError):
            node.to_html()