from FileSystemWatcher import * 
import os, sys
import os.path
from BlackList import *

notify(Watcher(), OsWatcher(), sys.argv[1]) 

for actual, swap in index.sync():
    actual = actual[:-1].replace("//", "/")
    swap = swap.replace("//", "/")
    print "Actual, swap: {} {}".format(actual, swap)
    if not os.path.isfile(actual) or os.path.isfile(swap):
        print "Is not a file"
    if swap is None:
        print "Should delete {}".format(actual)
    print "Blacklisting..."
    blacklist(actual)
    print "Renaming..."
    os.rename(swap, actual) 
    print "Done renaming"

