#!/usr/bin/python

import sys, os
import time

from TPGEgeneration import TPGEgeneratePages
from TPGEgeneration import TPGEcreateXML



import argparse

parser = argparse.ArgumentParser(description='OOMLOUT-TPGE -- Webpage Generation Using XML and Templates')
parser.add_argument('-rm','--runMode', help='Sets the runmode for special circumstances (A -- Generate All)', required=False)
parser.add_argument('-bd','--baseDirectory', help='Base directory to be working from', required=False)

parser.add_argument('-of','--outputFile', help='Name of output file for single generation, name of directory for multiple output, can include %%ID%% to be replaced', required=False)
parser.add_argument('-xa','--xmlAddition', help='File extension for supplied xml files (default ".xml")', required=False)
parser.add_argument('-ex','--extraXML', help='List of files or directories (searched recursively) to include in the made xml file', required=False)
parser.add_argument('-id','--idString', help='The ID String to be used in generating files', required=False)
parser.add_argument('-tm','--template', help='The template', required=False)


args = vars(parser.parse_args())

#loading variables from comman line






runMode = ""
if args['runMode'] <> None:
	runMode = args['runMode']

idString= "%%ID%%"
if args['idString'] <> None:
	idString = args['idString']
	idString = idString.replace("%%ID%%", idString)


baseDirectory=""
if args['baseDirectory'] <> None:
	baseDirectory = args['baseDirectory']
	baseDirectory = baseDirectory.replace("%%ID%%", idString)

if args['outputFile'] <> None:
	outputFile = args['outputFile']
	outputFile = outputFile.replace("%%ID%%", idString)

xmlAdd = ".xml"
if args['xmlAddition'] <> None:
	xmlAdd = args['xmlAddition']
	xmlAdd = xmlAdd.replace("%%ID%%", idString)

extraXML = ""
if args['extraXML'] <> None:
	extraXML = args['extraXML']
	extraXML = extraXML.replace("%%ID%%", idString)

template= "template/TEST-template.tmpl"
if args['template'] <> None:
	template = args['template']
	template = template.replace("%%ID%%", idString)


print runMode

def TPGEgenerateAllPages(baseDirectory, xmlAdd, template, outputFile, extraXML):
	print "Generating All OOMP Files:"
	TPGEcreateXML("", baseDirectory, xmlAdd, baseDirectory)

	for x in os.walk(baseDirectory):
		idString = str(x[0].replace(baseDirectory, ""))
		print "     Generating ---> " + idString
		outputFile2 = outputFile.replace("%%ID%%", idString)
		if idString <> "" :
			TPGEgeneratePages(idString, baseDirectory + idString + "/", xmlAdd, baseDirectory, template, outputFile2)


if runMode == "A" or runMode == "ALL":
	TPGEgenerateAllPages(baseDirectory, xmlAdd, template, outputFile, extraXML)
else:
	print ("Generating Pages: idString = " + idString + "  baseDirectory = " + baseDirectory + "  Template: " + template)
	TPGEcreateXML(idString, baseDirectory, xmlAdd, extraXML)
	TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML, template, outputFile)