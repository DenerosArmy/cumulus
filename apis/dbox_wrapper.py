import appkeys
from dropbox import client, rest, session

class DropboxService(object):
    def __init__(self):
        sess = session.DropboxSession(appkeys.DROPBOX['key'], \
                appkeys.DROPBOX['secret'], 'app_folder')
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        print("url: " + url)
        print("Please visit this site and press the 'Allow' button. Press enter when finished")
        raw_input()
        access_token = sess.obtain_access_token(request_token)
        self.client = client.DropboxClient(sess)
        print("Linked account")

    def upload(self, path):
        f = open(path)
        response = self.client.put_file(path.split('/')[-1], f)
        print("File uploaded successfully")

    def download(self, local_path, name):
        outFile = open(local_path, 'w')
        f, metadata = self.client.get_file_and_metadata(name)
        outFile.write(f.read())
        print("File downloaded successfully")
