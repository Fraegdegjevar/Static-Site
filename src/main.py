from textnode import *
from htmlnode import *
from convert_md_to_textnodes import *
from block_markdown import *
from generate_public import *
from generate_page import *

def main():
    copy_src_to_dest_dir("static", "public")
    generate_pages_recursive("content", "template.html", "public")

main()
