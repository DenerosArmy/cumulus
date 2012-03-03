"""
File Splitting Module

Input: path/to/file
Output: encrpyted file string portions

Output String format: file_name+file_index+string_portion

"""

from encrypter import encrypt, decrypt
from sys.path import insert
from os import rename, remove, abspath
insert(0, abspath(".."))
from os.path import join
#from indexer import index

def inform(cumulus_dir):
    global cumulus_directory
    cumulus_directory = cumulus_dir

cumulus_directory = "/home/jianwei/cumulus"

def get_rel_path(abs_path, folder_name="cumulus", delimiter="/"):
    """Changes the given absolute path to a path relative to the given folder name."""
    components = abs_path.split(delimiter)
    component = components.pop()
    rel_path = ""
    while component != folder_name:
        rel_path = component+delimiter+rel_path
        component = components.pop()
    return delimiter+rel_path

def get_abs_path(rel_path, folder_directory=cumulus_directory, delimiter="/"):
    """Changes the given relative path to an absolute path."""
    return cumulus_directory+rel_path

def add_metatags(file_path, index, contents):
    """Adds metatags to the contents."""
    return file_path+"|"+str(index)+"|"+contents

def retrieve_metatags(file_path):
    """Retrieves metatags from a given file path."""
    file_chunk = open(file_path)
    insides = file_chunk.readline()
    file_chunk.close()
    insides = insides.split("|")
    insides.pop(0)
    index = insides.pop(0)
    file_chunk = insides.pop(0)
    while insides:
        file_chunk+='|'+insides.pop(0)
    return int(index), file_chunk

def delete_file(file_path):
    """Deletes a file from the cloud storage."""
    pass

def rename_file(file_path, new_name):
    """Renames a file."""
    pass

def process_ram_file(ram_file_path):
    """Converts the given RAM file into a relative path."""
    rel_path = ram_file_path[9:].replace("_!_", "/")
    i = len(rel_path)-1
    while i >= 0:
        if rel_path[i] == "/": return rel_path[:i]
        i -= 1

def split_file(file_path, encrypt=False):
    """Takes in a file path, encrypts it if required, and outputs a set of split file path."""
    print("Split file is run")
    original_file = open(file_path, 'r')
    file_contents = original_file.readlines()
    original_file.close()
    temp_paths = set()
    rel_file_path = get_rel_path(file_path)
    for i in range(0, len(file_contents)):
        temp_file_path = "/dev/shm/"+rel_file_path.replace("/", "_!_")+str(i)+".temp"
        temp_file = open(temp_file_path, 'w')
        line = file_contents[i]
        if encrypt: line = encrypt(line)
        temp_file.write(add_metatags(file_path, i, line))
        temp_file.close()
        temp_paths.add(temp_file_path)
    print(temp_paths)
    return temp_paths

def join_file(rel_file_path, temp_file_paths):
    """Joins the files given by temp_file_paths, and writes the new file to the path given by the relative path."""
    chunks = {}
    for temp_file in temp_file_paths:
        index, file_chunk = retrieve_metatags(temp_file)
        chunks[index] = file_chunk
        remove(temp_file)
    temp_file_path = cumulus_directory+process_ram_file(rel_file_path)+".cumuluswap"
    temp_file = open(temp_file_path, 'w')
    for i in range(0, len(chunks)):
        temp_file.write(decrypt(chunks[i]))
    return get_absolute_path(rel_file_path), temp_file_path
    #rename(temp_file_path, get_abs_path(rel_file_path))

#index.set_read_file_cb(join_file)

'''
def upload_file(file_path, encrypt=False):
    """Upload the given file path to the cloud."""
    temp_file_paths = split_file(file_path, encrypt)
    return write_file(get_rel_path(file_path), temp_file_paths)
'''

from os.path import abspath
