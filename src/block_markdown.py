from textnode import *
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
        
    