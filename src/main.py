from textnode import *
from htmlnode import *
from functools import reduce


def main():
    test_text_node = TextNode("This is some test text", TextType.BOLD, "http://google.co.uk")
    print(test_text_node)
    test_html_node = HTMLNode(props = {"href": "https://www.google.com","target": "_blank", "img": "no_image"})
    print(test_html_node)
    #print(test_html_node)

main()
