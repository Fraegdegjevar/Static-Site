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

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        split_strings = [node.text]
        matches = extract_markdown_images(node.text)
        
        for match in matches:
            match_strings = reduce(lambda acc, string: acc + [string] if isinstance(string, TextNode) else acc + list(string.partition(f'![{match[0]}]({match[1]})')), split_strings, [])
            split_strings = [x for x in match_strings if x != '']
            
        for i in range(0, len(split_strings)):
            match = extract_markdown_images(split_strings[i])
            if len(match) == 1:
                new_nodes.append(TextNode(text = match[0][0], text_type = TextType.IMAGE, url = match[0][1]))
            else:
                new_nodes.append(TextNode(text = split_strings[i], text_type = TextType.TEXT))
    return new_nodes

def split_node_text_on_images(node_text):
    matches = extract_markdown_images(node_text)
    split_string = [node_text]
    node_list = []
    
    for match in matches:
        match_split = []
        for string in split_string:
            local_string = string.split(f'![{match[0]}]({match[1]})')
            if len(local_string) == 1:
                match_split.extend(local_string)
            else:
                local_string.insert(1, f'![{match[0]}]({match[1]})')
                match_split.extend([x for x in local_string if x != ''])
        split_string = match_split
    
    for string in split_string:
        match = extract_markdown_images(string)
        if len(match) == 1:
            node_list.append(TextNode(text = match[0][0], text_type = TextType.IMAGE, url = match[0][1]))
        else:
            node_list.append(TextNode(text = string, text_type=TextType.TEXT))
    return node_list

def split_node_text_on_links(node_text):
    matches = extract_markdown_links(node_text)
    split_string = [node_text]
    node_list = []
    
    for match in matches:
        match_split = []
        for string in split_string:
            local_string = string.split(f'[{match[0]}]({match[1]})')
            if len(local_string) == 1:
                match_split.extend(local_string)
            else:
                local_string.insert(1, f'[{match[0]}]({match[1]})')
                match_split.extend([x for x in local_string if x != ''])
        split_string = match_split
    
    for string in split_string:
        match = extract_markdown_links(string)
        if len(match) == 1:
            node_list.append(TextNode(text = match[0][0], text_type = TextType.LINK, url = match[0][1]))
        else:
            node_list.append(TextNode(text = string, text_type=TextType.TEXT))
    return node_list

def split_nodes_image2(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_list = split_node_text_on_images(node.text)
        new_nodes.extend(node_list)
    return new_nodes
            
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        node_list = split_node_text_on_links(node.text)
        new_nodes.extend(node_list)
    return new_nodes
    
            
            
            
        
        