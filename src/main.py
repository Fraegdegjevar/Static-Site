from generate_public import *
from generate_page import *
import sys

if len(sys.argv) > 1:
    basepath = sys.argv[1]
else:
    basepath = "/"

def main():
    copy_src_to_dest_dir("static", "docs")
    print(f"generating pages to basepath: {basepath}")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
main()
