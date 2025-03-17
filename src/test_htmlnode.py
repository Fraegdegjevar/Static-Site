import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props = {})
        node2 = HTMLNode(props = {})
        self.assertEqual(node, node2)
        
    def test_eq2(self):
        node = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = HTMLNode(tag = "a", value = "c", children = "c", props = {"a": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        self.assertNotEqual(node, node2)
    
    def test_not_eq2(self):
        node = HTMLNode(tag = "a", value = "b", children = "c", props = {"b": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        self.assertNotEqual(node, node2)
    
    def test_not_eq3(self):
        node = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c")
        self.assertNotEqual(node, node2)
    
    def test_props_to_html(self):
        node = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        self.assertEqual(node.props_to_html(), ' a="b" c="d"')
    
    def test_props_to_html2(self):
        node = HTMLNode(props = {})
        self.assertEqual(node.props_to_html(), '')
    
    def test_props_to_html3(self):
            node = HTMLNode()
            self.assertEqual(node.props_to_html(), '')

    def test_props_to_html4(self):
        node = HTMLNode(tag = "a", value = "g", children = "y", props = {"a": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
    
    def test_props_to_html5(self):
        node = HTMLNode(tag = "a", value = "b", children = "c", props = {"a": "b", "c": "d"})
        node2 = HTMLNode(tag = "a", value = "b", children = "c", props = {"x": "y", "c": "d"})
        self.assertNotEqual(node.props_to_html(), node2.props_to_html())
        
    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

if __name__ == "__main__":
    unittest.main()