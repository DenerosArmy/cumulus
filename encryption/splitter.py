"""
File Splitting Module

Input: path/to/file
Output: encrpyted file string portions

Output String format: file_name+file_index+string_portion

"""

from encryption import encrypt
from os.path import join 

def get_relative_path(abs_path, folder_name, delimiter="/"):
    """Changes the given absolute path to a path relative to the given folder name."""
    components = abs_path.split(delimiter)
    component = components.pop()
    rel_path = ""
    while component != folder_name:
        rel_path = component+delimiter+rel_path
        component = components.pop()
    return delimiter+rel_path

def add_metatags(file_path, index, contents):
    """Adds metatags to the contents."""
    return file_path+"|"+str(index)+"|"+contents

def retrieve_metatags(string):
    """Retrieves metatags from a given string."""
    while 

def delete_file(file_path):
    """Deletes a file from the cloud storage."""
    pass

def rename_file(file_path, new_name):
    """Renames a file."""
    pass

def split_file(file_path, encrypt):
    """Takes in a file path, encrypts it if required, and outputs a set of split file path."""
    original_file = open(file_path, 'r')
    file_contents = original_file.readlines()
    original_file.close()
    temp_paths = set()
    for i in range(0, len(file_contents)):
        temp_file_path = "/dev/shm/"+<file_path>+str(i)+".temp"
        temp_file = open(temp_file_path, 'w')
        line = file_contents[i]
        if encrypt: line = encrypt(line)
        temp_file.write(add_metatags(file_path, i, line))
        temp_file.close()
        temp_paths.add(temp_file_path)
    return temp_paths

def upload_file(file_path, encrypt=True):
    """Upload the given file path to the cloud."""
    temp_file_paths = split_file(file_path, encrypt)
    return write_file(<rel_path>, temp_file_paths)
    
