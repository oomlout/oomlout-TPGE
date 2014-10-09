#!/usr/bin/python

import sys

from TPGEgeneration import TPGEgeneratePages


#Print the help string
def printHelp():
	print ('OOMLOUT-TPGE -- Webpage Generation Using XML and Templates')

# Get the arguments list
argSize = len(sys.argv)

print ('Running Generation:   ' + ', '.join(sys.argv))

runMode = ""
idString= ""
baseDirectory=""
xmlAdd = "-XML.xml"
extraXML = ""

for t in sys.argv:
	print(t)

if argSize  > 1:
	runMode = str(sys.argv[1]).upper()
	idString = str(sys.argv[1]).upper()
if argSize  > 2:
	baseDirectory = str(sys.argv[2])
if argSize  > 3:
	xmlAdd = str(sys.argv[3])
if argSize  > 3:
	extraXML = str(sys.argv[4])




if runMode == "-H" or runMode == "-HELP":
	printHelp()
else:
	print ("Generating Pages: idString = " + idString + "  baseDirectory = " + baseDirectory)
	TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML)

