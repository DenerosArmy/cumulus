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

    def set_read_file_cb(self, cb):
        """Set the callback when a file on the cloud is added or updated
        The callback is called with the proper name of the file
        (the name on the actual filesystem), a list of filepaths to new/updated chunks
        of the file, and a list of filepaths to chunks of the file that have remained
        unchanged.

        :param function cb: The callback, of the form function(proper_name, new_chunks, old_chunks):
        """
        self.read_file_cb = cb

    def write_file(self, proper_name, chunks):
        """Write a file to the cloud

        :param proper_name: Proper name of the file (actual path on the filesystem, relative to folder we're tracking)
        :param chunks: Iterable of absolute paths to chunks of the file
        """
        pass

    def rename_file(self, old_name, new_name):
        """Signal a file rename

        :param old_name: Old proper name of the file
        :param new_name: New proper name of the file
        """
        pass

    def delete_file(self, proper_name):
        """Signal a file delete

        :param proper_name: Proper name of the file to be deleted
        """
        pass
