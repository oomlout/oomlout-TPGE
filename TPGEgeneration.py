from TPGExml import TPGEgetValueExtra
from TPGExml import TPGEgetValue
from TPGExml import TPGEgetValueWhere
import sys
import time
from TPGExml import TPGEgetAllFilesIterate

import xml.etree.ElementTree as ET
import os.path

templateFileName = "template/PROJ-template.tmpl"

tempCombinedXMLFileName = "tmp/tempCombinedXML.xml"



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




# Main Routine
def TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML):
	print ("  TPGE -- Generating Pages")

	root = TPGELoadXML(idString, baseDirectory, xmlAdd, extraXML)



	#def TPGEgetValueExtra(lookupString, tree, testValue, returnValue)

	lookupString = "oompTag.tagName"
	testValue = "oompColor"
	returnValue = "tagReadable"

	value = TPGEgetValueExtra(lookupString, root, testValue, returnValue)
	print("********************* VALUE ********* " + value)



	#getting template name trying in ID directory
	##Need to ad a for each
	templateFileName = baseDirectory + TPGEgetValue("basics.template", root)
	try:
		templateFile = open(templateFileName,"r")
	except IOError:
		try:
			templateFileName = TPGEgetValue("basics.template", root)
			templateFile = open("template/" + templateFileName,"r")
		except IOError:
			templateFileName = "template/TEST-template.tmpl"
			templateFile = open("template/TEST-template.tmpl","r")

	print "Using Template:  " + templateFileName

	outputFileName = TPGEgetValue("basics.output", root)
	if outputFileName == "":
		outputFileName = "index.html"
	print "Outputing File:  " + baseDirectory + outputFileName
	outputFile = open(baseDirectory + outputFileName, "w+")


	#replaceTags
	for line in templateFile.readlines():

		includeLine = True

		##REPLACE ALL TAGS FIRST
		if includeLine:
			#####REPLACE TAGS
			#Replace all occurances of ID
			line = line.replace("%%ID%%", idString)

			while find_between(line, "@@", "@@") != "":
				#find first tag
				tag = find_between(line, "@@", "@@")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@

				value = TPGEgetValueWhere(details[0], root, details[1], details[2])

				print "Replacing Tag " + tag + "   " + value[0:20]
				line = line.replace("@@" + tag + "@@", value)


		##AFTER REPLACMENT TEST FOR INCLUSION
		if line[:1] == "#":
			#skip line as template comment
			#print"Skipping Line   COMMENT    " + line[0:20]
			includeLine = False
		elif line[:1] == "^":
			#Test for file existance id directory based
			testFile =find_between(line, "^^", "^^")
			if os.path.isfile(baseDirectory + testFile):
				line = line.replace("^^" + testFile + "^^", "")
				includeLine = True
			else:
				print"Skipping Line   FILE DOESN'T EXIST    " + line[0:20]
				includeLine = False
		elif line[:1] == "*":
			#Test for tag existance id directory based
			testTag = find_between(line, "**", "**")

			value = TPGEgetValue(testTag, root)
			if value <> "":
				line = line.replace("**" + testTag + "**", "")
				includeLine = True
			else:
				print"Skipping Line   TAG DOESN'T EXIST    " + line[0:20]
				includeLine = False
		else:
			r=7

		if includeLine:
			outputFile.write(line)
	outputFile.close()


def TPGELoadXML(idString, baseDirectory, xmlAdd, extraXML):

	xmlFileName = TPGEgetAllFilesIterate("tags/", ".xml")

	fileList = extraXML.split(",")

	moreXML = []

	for item in fileList:
		if os.path.isdir(item):
			moreXML = moreXML + TPGEgetAllFilesIterate(item, xmlAdd)
			moreXML = moreXML + TPGEgetAllFilesIterate(item, ".xml")
		else:
			moreXML.append(item)
	moreXML = moreXML + xmlFileName

	return TPGELoadXMLList(moreXML)



def TPGELoadXMLList(list):
	xmlFiles = list
	f = open(tempCombinedXMLFileName,'w+')
	f.write("<xml>")

	print ("Loading XML FILES:  ")
	print "---------"
	for item in xmlFiles:
		#print "Loading File    " + item
		for line in open(item):
			if ("<xml>" in line) or ("</xml>" in line):
				t = 0
		#		sys.stdout.write("S")
			else:
				f.write(line)
		#		sys.stdout.write(".")
		#print ""
	f.write("</xml>")
	f.close()
	tree = ET.parse(tempCombinedXMLFileName)
	return tree.getroot()



