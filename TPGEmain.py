#!/usr/bin/python

import sys, os
import time

from TPGEgeneration import *
from TPGEgeneration import TPGEgeneratePages
from TPGEgeneration import TPGEcreateXML
from TPGExml import *


import argparse

parser = argparse.ArgumentParser(description='OOMLOUT-TPGE -- Webpage Generation Using XML and Templates')
parser.add_argument('-rm','--runMode', help='Sets the runmode for special circumstances (A -- Generate All)', required=False)
parser.add_argument('-bd','--baseDirectory', help='Base directory to be working from', required=False)

parser.add_argument('-of','--outputFile', help='Name of output file for single generation, name of directory for multiple output, can include %%ID%% to be replaced', required=False)
parser.add_argument('-xa','--xmlAddition', help='File extension for supplied xml files (default ".xml")', required=False)
parser.add_argument('-ex','--extraXML', help='List of files or directories (searched recursively) to include in the made xml file', required=False)
parser.add_argument('-id','--idString', help='The ID String to be used in generating files', required=False)
parser.add_argument('-tm','--template', help='The template', required=False)
parser.add_argument('-ui','--uniqueID', help='Us a unique ID rather than directory srtructire for IDs', required=False)


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

uID = ""
if args['uniqueID'] <> None:
	uID = args['uniqueID']
	

	

print runMode

def TPGEgenerateAllPages(baseDirectory, xmlAdd, template, outputFile, extraXML):
	print "Generating All OOMP Files:"
	TPGEcreateXML("", baseDirectory, xmlAdd, extraXML)
	TPGEcreateXML("", baseDirectory, xmlAdd, extraXML)
	root2 = TPGEloadXML()
	for x in os.walk(baseDirectory):
		idString = str(x[0].replace(baseDirectory, ""))
		print "  TPGE-Generating ---> " + idString
		outputFile2 = outputFile.replace("%%ID%%", idString)
		outputFile2 = TPGEreplaceLine(idString, outputFile2, root2, baseDirectory)
		
		#remove any tags in the filename
		outputFileTest=outputFile
		#outputFileTest=outputFile.replace("%%ID%%", idString) #replace ID 
		while find_between(outputFileTest, "@@", "@@") != "":
			tag = find_between(outputFileTest, "@@", "@@")
			outputFileTest = outputFileTest.replace("@@" + tag + "@@","") #replace tag with nothing to simulate receiving no replacement when TPGEreplacinglines
			
		print "---------------------------------------------"
		print outputFileTest
		print outputFile2
		print "---------------------------------------------"
		
		if idString <> "" and not outputFile2 in outputFileTest:
			TPGEgeneratePages(idString, baseDirectory + idString + "/", xmlAdd, baseDirectory, template, outputFile2)
		else:
			print "NOT CREATING FILE DUE TO BLANK FILENAME"
			print "NOT CREATING FILE DUE TO BLANK FILENAME"
			print "NOT CREATING FILE DUE TO BLANK FILENAME"

def TPGEgenerateAllPagesUID(baseDirectory, xmlAdd, template, outputFile, extraXML):
	print "Generating All Files UID:"
	TPGEcreateXML("", baseDirectory, xmlAdd, extraXML)
	root2 = TPGEloadXML()
	for x in range(0,10000):
		#TPGEgetValueIndex(index, tree, testField, resultField):
		print "  Starting" 
		end = uID.split(".")[1]
		idString = TPGEgetValueIndex(x, root2, uID, end)
		print "  TPGE-Generating ---> " + idString
		outputFile2 = outputFile.replace("%%ID%%", idString)
		#TPGEreplaceLine(idString, runLine, root, baseDirectory)
		outputFile2 = TPGEreplaceLine(idString, outputFile2, root2, baseDirectory)
		if idString <> "" :
			TPGEgeneratePages(idString, baseDirectory + idString + "/", xmlAdd, baseDirectory, template, outputFile2)

			

if runMode == "A" or runMode == "ALL":
	TPGEgenerateAllPages(baseDirectory, xmlAdd, template, outputFile, extraXML)
elif uID <> "":
	TPGEgenerateAllPagesUID(baseDirectory, xmlAdd, template, outputFile, extraXML)
else:
	print ("Generating Pages: idString = " + idString + "  baseDirectory = " + baseDirectory + "  Template: " + template)
	TPGEcreateXML(idString, baseDirectory, xmlAdd, extraXML)
	TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML, template, outputFile)