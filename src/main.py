from textnode import *
from htmlnode import *
from convert_md_to_textnodes import *
from block_markdown import *
from generate_public import *

def main():
    copy_src_to_dest_dir("static", "public")

main()
