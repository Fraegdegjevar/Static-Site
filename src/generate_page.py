from block_markdown import *
from generate_public import *
import re
import os
import shutil

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No title header in markdown file!")
    
def generate_page(from_path, template_path=None, dest_path=None):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    
    html_content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    
    template_with_content = re.sub("{{ Content }}", html_content, template)
    template_with_title = re.sub("{{ Title }}", title, template_with_content)
    
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)  
    
    with open(dest_path, 'w') as f:
        f.write(template_with_title)
        f.close()
    
    
    
    
    
