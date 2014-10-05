#!/usr/bin/python

import sys

from TPGEgeneration import TPGEgeneratePages


#Print the help string
def printHelp():
	print ('OOMLOUT-TPGE -- Webpage Generation Using XML and Templates')





id = "WHSN"

# Get the total number of args passed to the demo.py
total = len(sys.argv)

# Get the arguments list
cmdargs = str(sys.argv)

# Print it
print ("The total numbers of args passed to the script: %d " % total)


argSize = len(sys.argv)

runMode = ""

if argSize  > 1:
	runMode = str(sys.argv[1]).upper()

if runMode == "-H" or runMode == "-HELP":
	printHelp()
else:
	TPGEgeneratePages(id)

