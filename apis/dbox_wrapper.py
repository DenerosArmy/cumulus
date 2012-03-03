import appkeys
from dropbox import client, rest, session
import os
import time

class DropboxService(object):

    lastIndexMetadata = {'modified':''}

    def __init__(self):
        sess = session.DropboxSession(appkeys.DROPBOX['key'], \
                appkeys.DROPBOX['secret'], 'app_folder')
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        os.system("xdg-open {0}".format(url))

        print("Press enter when authentication has completed")
        raw_input()

        access_token = sess.obtain_access_token(request_token)
        self.client = client.DropboxClient(sess)
        print("Linked account")

    def upload(self, path):
        f = open(path)
        metadata = self.client.put_file(os.path.basename(path), f, True)
        print("File uploaded successfully")

    def download(self, local_path, name):
        outFile = open(local_path, 'w')
        f, metadata = self.client.get_file_and_metadata(name)
        outFile.write(f.read())
        print("File downloaded successfully")

    def uploadIndex(self, index_path):
        """Takes the local path of the index file"""
        f = open(index_path)
        self.lastIndexMetadata = self.client.put_file('index1234567890.json', f, True)

    def downloadIndex(self, index_path):
        indexFile = open(index_path, 'w')
        f = self.client.get_file('index1234567890.json')
        indexFile.write(f.read())

    def isChangedIndex(self):
        serverData = self.client.metadata('index1234567890.json')
        if serverData['modified']==self.lastIndexMetadata['modified']:
            return False
        else:
            return True
