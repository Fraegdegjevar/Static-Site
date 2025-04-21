import os
import shutil

def copy_src_to_dest_dir(source_dir, dest_dir):
    if not os.path.exists(source_dir):
        raise Exception('Source directory does not exist.')
    
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)
        print(f"FOUND dest_dir: {dest_dir}. CLEARING CONTENTS")
        os.mkdir(dest_dir)
    else:
        os.mkdir(dest_dir)
        print(f"CREATING {dest_dir}")
    
    for item in os.listdir(source_dir):
        obj_path = os.path.join(source_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(obj_path):
            shutil.copy(obj_path, dest_path)
            print(f"COPY FILE: {obj_path} -> {dest_path}")
        else:
            print(f"DIRECTORY FOUND: {obj_path}, WALKING:")
            copy_src_to_dest_dir(obj_path, dest_path)