#!/usr/bin/python

import sys, os
import time

from TPGEgeneration import TPGEgeneratePages
from TPGEgeneration import TPGEcreateXML
from TPGEgeneration import TPGEgenerateDirectory

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

	working = str(sys.argv[2])
	working = working.replace("%ID%", idString)
	baseDirectory = working
if argSize  > 3:
	working = str(sys.argv[3])
	working = working.replace("%ID%", idString)
	xmlAdd = working
if argSize  > 3:
	working = str(sys.argv[4])
	working = working.replace("%ID%", idString)
	extraXML = working
if argSize  > 4:
	working = str(sys.argv[5])
	working = working.replace("%ID%", idString)
	template = working
if argSize  > 5:
	working = str(sys.argv[6])
	working = working.replace("%ID%", idString)
	output = working


def TPGEgenerateAllPages(baseDirectory):
	TPGEgenerateDirectory(baseDirectory)
	print "Generating All OOMP Files:"
	TPGEcreateXML("", baseDirectory, ".oomp", baseDirectory)

	for x in os.walk(baseDirectory):
		idString = str(x[0].replace(baseDirectory, ""))
		print "     Generating ---> " + idString
		if idString <> "" :
			TPGEgeneratePages(idString, baseDirectory + idString + "/", ".oomp", baseDirectory, "template/OOMP-template.tmpl", idString + ".html")


if runMode == "-H" or runMode == "-HELP":
	printHelp()
elif runMode == "-A" or runMode == "-ALL":
	TPGEgenerateAllPages(baseDirectory)
else:
	print ("Generating Pages: idString = " + idString + "  baseDirectory = " + baseDirectory + "  Template: " + template)
	TPGEcreateXML(idString, baseDirectory, xmlAdd, extraXML)
	TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML, template, output)