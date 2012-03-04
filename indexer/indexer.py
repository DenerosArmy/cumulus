import os, sys
import os.path
import json
sys.path.insert(0, os.path.abspath('..'))
from apis.dbox_wrapper import DropboxService
import time

class Index(object):
    """An index of mappings between local files and files in the cloud
    """

    def __init__(self):
        """Initialize the index
        """
        def cb(proper_name, new_chunks, old_chunks):
            print "Remote updated file {}: new chunks {}, old chunks {}".format(
                proper_name, new_chunks, old_chunks)
            return "@@fake-path", "@@fake-path"
        self.read_file_cb = cb

        def cb(proper_name):
            print "Remote deleted file {}".format(proper_name)
            return "@@fake-path", None
        self.read_delete_file_cb = cb

        self.backends = { "db" : DropboxService() }

        self.json_counter = 0

        self.pull_json()

        self.mapping = {}
        self.idx_json = {}

    def set_read_file_cb(self, cb):
        """Set the callback when a file on the cloud is added or updated
        The callback is called with the proper name of the file
        (the name on the actual filesystem), a list of filepaths to new/updated chunks
        of the file, and a list of filepaths to chunks of the file that have remained
        unchanged.

        :param function cb: The callback, of the form function(proper_name, new_chunks, old_chunks):
        """
        self.read_file_cb = cb

    def set_read_delete_file_cb(self, cb):
        """Set the callback when a file on the cloud is deleted
        The callback is called with the proper name of the file
        (the name on the actual filesystem)

        :param function cb: The callback, of the form function(proper_name):
        """
        self.read_delete_file_cb = cb

    def write_file(self, proper_name, chunks):
        """Write a file to the cloud

        :param proper_name: Proper name of the file (actual path on the filesystem, relative to folder we're tracking)
        :param chunks: Iterable of absolute paths to chunks of the file
        """
        for chunk in chunks:
            print "Uploading chunk: {}".format(chunk)
            self.backends["db"].upload(chunk)

        self.mapping[proper_name] = [ os.path.basename(chunk) for chunk in chunks ]
        self.idx_json[unicode(self.json_counter)] = [
            {
            'file' : proper_name,
            'chunks' : self.mapping[proper_name]
            }
            ]
        self.json_counter += 1
        self.push_json()

    def rename_file(self, old_name, new_name):
        """Signal a file rename

        :param old_name: Old proper name of the file
        :param new_name: New proper name of the file
        """
        self.mapping[new_name] = self.mapping[old_name]
        del self.mapping[old_name]

        self.idx_json[unicode(self.json_counter)] = [
            {
            'file' : old_name,
            'chunks' : None
            },
            {
            'file' : new_name,
            'chunks' : self.mapping[new_name]
            }
            ]
        self.json_counter += 1
        self.push_json()

    def delete_file(self, proper_name):
        """Signal a file delete

        :param proper_name: Proper name of the file to be deleted
        """
        del self.mapping[proper_name]

        self.idx_json[unicode(self.json_counter)] = [
            {
            'file' : proper_name,
            'chunks' : None
            }
            ]
        self.json_counter += 1
        self.push_json()

    def sync(self):
        """Syncs the remote data with the database. Yields (proper_name, swap_name pairs) whenever a file is updated"""
        while True:
            for x in self.pull_json():
                yield x

    def download_all(self):
        """Download all files from server"""
        self.mapping = {}
        self.idx_json = {}
        self.json_counter = 0

        for filepath, swappath in self.pull_json():
            print "Download {}<---{}".format(filepath, swappath)

    def push_json(self):
        """Push JSON to the JSON target backend
        """
        print "Pushing JSON: {}".format(json.dumps(self.idx_json))
        with open('/dev/shm/idx.json', 'w') as f:
            json.dump(self.idx_json, f)
        print "Uploading JSON"
        self.backends["db"].upload('/dev/shm/idx.json')
        print "Pushed JSON: {}".format(json.dumps(self.idx_json))

        print "Press enter to download everything"
        raw_input()
        self.json_counter = 0

    def pull_json(self):
        """Pull in new JSON data and update files on our end. Yields (filepath, swapfilepath) pairs.
        """
        try:
            self.backends["db"].download('/dev/shm/idx.json', 'idx.json')
        except:
            return

        with open('/dev/shm/idx.json') as f:
            try:
                new_json = json.load(f)
            except:
                print "JSON could not load: {}".format(f.read())
                return
        print "Pulled JSON: {}".format(new_json)

        while unicode(self.json_counter) in new_json.keys():
            new = new_json[unicode(self.json_counter)]
            print "New: {}".format(new)
            for datum in new:
                if datum['chunks'] is None:
                    print "Deleting file: {}".format(datum['file'])
                    del self.mapping[datum['file']]
                    yield self.delete_file_cb(datum['file'])
                else:
                    self.mapping[datum['file']] = datum['chunks']
                    # Download the chunks
                    for chunk in datum['chunks']:
                        print "Downloading chunk: {}".format(chunk)
                        self.backends["db"].download(os.path.join("/dev/shm", chunk), chunk)
                    yield self.read_file_cb(datum['file'], [os.path.join("/dev/shm", chunk) for chunk in datum['chunks']])
            self.json_counter += 1
        print "Current counter: {}".format(self.json_counter)

        self.idx_json = new_json
