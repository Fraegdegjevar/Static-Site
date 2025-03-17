import unittest
from htmlnode import *

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

class TestLeafNode(unittest.TestCase):
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
        node = LeafNode(tag = None, value = "No tags!")
        self.assertEqual(node.to_html(), "No tags!")
    
    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(None, None, None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_child_has_no_tag(self):
        child_node = ParentNode(None, [LeafNode("a", "hello!")] , None)
        node = ParentNode("div", [child_node], None)
        with self.assertRaises(ValueError):
            node.to_html()        
    
    def test_to_html_no_child(self):
        node = ParentNode("a", None, None)
        with self.assertRaises(ValueError):
            node.to_html()
            
    def test_to_html_child_has_no_child(self):
        child_node = ParentNode("span", None, None)
        node = ParentNode("div", [child_node], None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_child(self):
        child_node = LeafNode("a", "click here!", props = {"href": "will.co.uk"})
        node = ParentNode("div", [child_node], props = {"attr_a": "top_parent"})
        self.assertEqual(node.to_html(), '<div attr_a="top_parent"><a href="will.co.uk">click here!</a></div>')
        
    def test_to_html_children(self):
        child_node = LeafNode("a", "click here!", props = {"href": "will.co.uk"})
        child_node2 = LeafNode("b", "child2")
        node = ParentNode("div", [child_node, child_node2], props = {"attr_a": "top_parent"})
        self.assertEqual(node.to_html(), '<div attr_a="top_parent"><a href="will.co.uk">click here!</a><b>child2</b></div>')
    
    def test_to_html_grandchild(self):
        grandchild_node = LeafNode("a", "click here!", props = {"href": "will.co.uk"})
        child_node = ParentNode("span", [grandchild_node], props = {"attr_b": "mid_parent"})
        node = ParentNode("div", [child_node], props = {"attr_a": "top_parent"})
        self.assertEqual(node.to_html(), '<div attr_a="top_parent"><span attr_b="mid_parent"><a href="will.co.uk">click here!</a></span></div>')
        
    def test_to_html_grandchildren(self):
        grandchild_node = LeafNode("a", "grandchild1", props = {"href": "will.co.uk"})
        grandchild_node2 = LeafNode("b", "grandchild2")
        grandchild_node3 = LeafNode("c", "grandchild3", props = {"href": "gc3.co.uk"})
        grandchild_node4 = LeafNode("d", "grandchild4")
        child_node = ParentNode("span", [grandchild_node, grandchild_node2], props = {"attr_b": "mid_parent1"})
        child_node2 = ParentNode("class", [grandchild_node3, grandchild_node4], props = {"attr_c": "mid_parent2"})
        node = ParentNode("div", [child_node, child_node2], props = {"attr_a": "top_parent"})
        self.assertEqual(node.to_html(), '<div attr_a="top_parent"><span attr_b="mid_parent1"><a href="will.co.uk">grandchild1</a><b>grandchild2</b></span><class attr_c="mid_parent2"><c href="gc3.co.uk">grandchild3</c><d>grandchild4</d></class></div>')
        
        
if __name__ == "__main__":
    unittest.main()