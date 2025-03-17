from functools import reduce

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        return "" if not self.props else reduce(lambda acc, attr: f'{acc} {attr}="{self.props[attr]}"', self.props, "")
    
    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})'
    
    def __eq__(self, other):
        return (self.tag == other.tag and self.value == other.value 
        and self.children == other.children and self.props == other.props)

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag = tag, value = value, children = None, props = props)
    
    def to_html(self):
        if self.value == None:
            raise ValueError("Invalid HTML: must have a value")
        elif self.tag == None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag = tag, children = children, props = props)
        
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node must have a tag!")
        elif self.children is None:
            raise ValueError("Parent Node must have at least one child node!")
        else:
            child_html = ''.join(list(map(lambda child: child.to_html(), self.children)))
            return f'<{self.tag}{self.props_to_html()}>{child_html}</{self.tag}>'