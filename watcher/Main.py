from BlackList import *
for name in index.sync:
	actual = name[0] 
	swap = name[1] 
	blacklist(actual)
	rename(actual,swap) 


