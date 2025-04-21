from textnode import *
from convert_md_to_textnodes import *
from htmlnode import *
import re

def markdown_to_blocks(markdown):
    blocks = [block.strip() for block in markdown.split("\n\n") if block.strip()]
    return blocks

class BlockType(Enum):
    PARAGRAPH = "paragraph" 
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def block_to_blocktype(block):
    # First 1-6 chrs are # followed by a space - heading
    # re.match matches start of string only i.e ^ is implied in regex
    if re.match(r"#{1,6} ", block) != None:
        return BlockType.HEADING
    if block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    #Now we need to consider if the block is an (un)ordered list or quote which requires line by line 
    #inspection.  
    def check_lines_start_with(lines, start_char):
        for line in lines:
            if line[0:len(start_char)] != start_char:
                return False
        return True
    
    lines = block.split("\n")

    if check_lines_start_with(lines, ">"):
        return BlockType.QUOTE
    if check_lines_start_with(lines, "- "):
        return BlockType.UNORDERED_LIST
    
    #if any line starts fail criteria for ordered list, return the only remaining type possible,
    # paragraph.
    expected_num = 0
    for line in lines:
        line_start =  re.match(r"^(\d+)(\. )", line)
        if not line_start or int(line_start.group(1)) != expected_num + 1 or line_start.group(2) != ". ":
            return BlockType.PARAGRAPH
        expected_num += 1
    return BlockType.ORDERED_LIST

def block_text_to_children(block, ignore_markdown = False):
    lines = block.split("\n")
    child_nodes = []
    
    if ignore_markdown:
        for line in lines:
            child_node = TextNode(line, TextType.TEXT)
            child_nodes.append(text_node_to_html_node(child_node))
        return child_nodes
    
    for line in lines:
        # convert line to text nodes then convert them all to leaf nodes
        child_text_nodes = [text_node_to_html_node(leaf) for leaf in text_to_textnodes(line)] 
        child_nodes.extend(child_text_nodes)
    
    return child_nodes
        
def wrap_child_html_nodes(child_nodes, tag):
    wrapped_child_nodes = []
    for child in child_nodes:
        wrapped_child_nodes.append(ParentNode(tag = tag, children = child))
    return wrapped_child_nodes

def block_to_html_node(block):
    match (block_to_blocktype(block)):
        case (BlockType.QUOTE):
            block_text = "\n".join(line[1:] for line in block.splitlines())
            return ParentNode(tag="blockquote", children = block_text_to_children(block_text))
        case (BlockType.UNORDERED_LIST):
            block_text = "\n".join(line[2:] for line in block.splitlines())
            node_children = block_text_to_children(block_text)
            return ParentNode(tag="ul", children = wrap_child_html_nodes(node_children, "li"))
        case (BlockType.ORDERED_LIST):
            block_text = "\n".join(line[3:] for line in block.splitlines())
            node_children = block_text_to_children(block_text)
            return ParentNode(tag="ol", children = wrap_child_html_nodes(node_children, "li"))
        case (BlockType.CODE):
            block_text = block[3:-3]
            return ParentNode(tag="pre", children = ParentNode(tag="code", children = block_text_to_children(block_text, True)))
        case (BlockType.PARAGRAPH):
            return ParentNode(tag="p", children = block_text_to_children(block)) #no modification needed
        case (BlockType.HEADING):
            level = re.match(r"#{1,6}", block).group(0).count("#")
            block_text = block[level:]
            return ParentNode(tag=f"h{level}", children = block_text_to_children(block_text))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    
    for block in blocks:
        block_nodes.append(block_to_html_node(block))
    
    return ParentNode("div", block_nodes)
    
          
    