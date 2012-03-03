import os 
from pyinotify import *
sys.path.insert(0,os.path.abspath('..'))
from encryption.splitter import split_file 
 
import BlackList
''' Interface for watching file system, monitors specfic file/directory calls Spliiter upon any changes ''' 
def Watcher(): 
	return WatchManager() 
	

class OsWatcher(ProcessEvent):
    '''The processor class, handles certain inotify events and sends appropriate commands to Splitter. Each event has a particular code that it corresponds to'''
    mask =  EventsCodes.ALL_FLAGS['IN_CREATE'] | EventsCodes.ALL_FLAGS['IN_DELETE']  | EventsCodes.ALL_FLAGS['IN_MODIFY'] | EventsCodes.ALL_FLAGS['IN_MOVED_FROM']  | EventsCodes.ALL_FLAGS['IN_MOVED_TO']

    def process_IN_CREATE(self,event): 
	path = os.path.join(event.path,event.name) 
	split_file(os.path.join(event.path,event.name))
	print(path)
'''    
    def process_IN_DELETE(self,event):
	path = os.path.join(event.path,event.name) 
	if (path != dont_check && path[-11:] != ".cumuluswap"):
          delete_file(os.path.join(event.path,event.name))
	print(os.path.join(event.path,event.name)) 
    def process_IN_MODIFY(self,event): 
	path = os.path.join(event.path,event.name) 
#	if (path != dont_check && path[-11:] != ".cumuluswap"):
	    upload_file(os.path.join(event.path,event.name)) 
	print(os.path.join(event.path,event.name)) 
    def process_MOVED_FROM(self,event):
	path = os.path.join(event.path,event.name) 
	if (path != dont_check && path[-11:] != ".cumuluswap"):
	   delete_file(os.path.join(event.path,event.name))
	print(os.path.join(event.path,event.name)) 
    def process_MOVED_TO(self,event):
	path = os.path.join(event.path,event.name) 
	if (path != dont_check && path[-11:] != ".cumuluswap"):
 		upload_file(os.path,join(event.path,event.name)) 
   	print(os.path.join(event.path,event.name)) 
   ''' 

def notify(Watcher, Process, Path): 
	'''Instantiates notify class with the OsWatcher Process''' 
	#inform(path) 
	notifier = ThreadedNotifier(Watcher,Process) 
	notifier.start() 
	Watcher.add_watch(Path,OsWatcher.mask,rec=True)
	print(Path + " is now being tracked by Cumulus") 






