import os.path
import json

class Index(object):
    """An index of mappings between local files and files in the cloud
    """

    def __init__(self):
        """Initialize the index
        """
        def cb(proper_name, new_chunks, old_chunks):
            print "Remote updated file {}: new chunks {}, old chunks {}".format(
                proper_name, new_chunks, old_chunks)
        self.read_file_cb = cb

        def cb(proper_name):
            print "Remote deleted file {}".format(proper_name)
        self.read_delete_file_cb = cb

        self.mapping = {}
        self.idx_json = {}
        self.json_counter = 0

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
            print "Fake uploading chunk: {}".format(chunk)
            #<backingstore>.upload(chunk)
            #TODO: upload chunk
            pass

        self.mapping[proper_name] = [ os.path.basename(chunk) for chunk in chunks ]
        self.idx_json[self.json_counter] = [
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

        self.idx_json[self.json_counter] = [
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

        self.idx_json[self.json_counter] = [
            {
            'file' : proper_name,
            'chunks' : None
            }
            ]
        self.json_counter += 1
        self.push_json()

    def sync_remote_updated(self):
        """Call to sync the index when the remote index is updated"""
        self.pull_json()


    def push_json(self):
        """Push JSON to the JSON target backend
        """
        #TODO: push JSON
        #<json_backend>.write_data(json.dumps(self.idx_json))
        print "Fake pushing JSON: {}".format(json.dumps(self.idx_json))

    def pull_json(self):
        """Pull in new JSON data and update files on our end
        """
        new_json = []
        #TODO: pull JSON
        print "Fake pulling JSON: {}".format(new_json)
        #new_json = json.loads(<json_backend>.read_data())
        while self.json_counter in new_json.keys():
            new = new_json[self.json_counter]
            for datum in new:
                if datum['chunks'] is None:
                    del self.mapping[datum['file']]
                    self.delete_file_cb(datum['file'])
                else:
                    self.mapping[datum['file']] = datum['chunks']
                    self.read_file_cb(datum['file'], datum['chunks'], [])
            self.json_counter += 1
