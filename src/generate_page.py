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
    
def generate_page(from_path, template_path, dest_path, basepath):
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
    template_with_title = template_with_title.replace('href="/', f'href="{basepath}')
    template_with_title = template_with_title.replace('src="/', f'src="{basepath}')
    
    os.makedirs(os.path.dirname(dest_path), exist_ok = True)  
    
    with open(dest_path, 'w') as f:
        f.write(template_with_title)
        f.close()

def generate_pages_recursive(dir_path_content, template_path,  dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        item_dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(item_path):
            generate_page(item_path,template_path, item_dest_path.replace("md", "html"), basepath)
        else:
            print(f"Entering directory: {item_path}")
            generate_pages_recursive(item_path, template_path, item_dest_path, basepath)