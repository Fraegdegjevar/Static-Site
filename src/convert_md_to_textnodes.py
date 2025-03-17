from textnode import *
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or node.text.count(delimiter) == 0:
            new_nodes.append(node)
        elif node.text.count(delimiter) % 2 != 0:
            raise Exception("Invalid Markdown! Mismatching delimiters. Did you forget a closing delimiter?")
        else:
            split_strings = node.text.split(delimiter)
            # As we have no nesting - if we have an even number of delimiters, and want to handle
            # multiple sets of non-nested delimiters across the text string, then structure will be (use * as delim in example)
            #before_delim*between_delim*after_delim*between_delim*after_delim -> even indexes are outside delims,
            # odd indexes are inside delims in the split string list
            for i in range(0,len(split_strings)):
                split_strings[i] = TextNode(text = split_strings[i], text_type = TextType.TEXT if i % 2 == 0 else text_type)
            new_nodes.extend(split_strings)
                
    return new_nodes
