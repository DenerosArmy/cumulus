from BoxAPI import *
import appkeys

class BoxService(object):

    def __init__(self):
        self.box = BoxDotNet()
        self.token = self.box.login(appkeys.BOX['key'])


    def upload(self, path):
        self.box.upload(path)
