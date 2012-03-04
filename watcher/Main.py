from BlackList import *
from os import rename

for name in index.sync():
	actual = name[0] 
	swap = name[1] 
	blacklist(actual)
	rename(actual,swap) 


