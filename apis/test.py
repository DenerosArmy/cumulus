from dbox_wrapper import DropboxService
from box_wrapper import BoxService

def main():
    """
    dbox = DropboxService()
    dbox.upload('test/testfile.txt')
    dbox.download('test/testfile_downloaded.txt', 'testfile.txt')

    dbox.uploadIndex('test/index.txt')
    print(dbox.isChangedIndex())
    dbox.downloadIndex('test/index.txt')
    """
    box = BoxService()
    box.upload('test/testfile.txt')

main()
