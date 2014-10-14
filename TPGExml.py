import xml.etree.ElementTree as ET

xmlFileName = "tags/TPGE-oomlout-tags.xml"

xmlIDBase = "c:/GH/oomlout-"

def TPGEgetValue(lookupString, tree):
	xmlLookup = lookupString.split(".")
	for tag in xmlLookup:
		try:
			value = tree.find(tag).text
		except AttributeError:
			value = ""
		try:
			tree = tree.find(tag)
		except AttributeError:
			value = ""

	if value is None:
		print "    TAG NOT FOUND  " + lookupString
		value = ""

	return value

def TPGEgetValueExtra(lookupString, tree, testValue, returnValue):


	xmlLookup = lookupString.split(".")
	for tag in xmlLookup:
		try:
			#try and find the text if not found try and go down one step
			value = tree.findall(tag)
		except AttributeError:
			value = ""
		try:
			#text not found go down on step of the tree and try again
			tree = tree.findall(tag)
		except AttributeError:
			value = ""

	#TEST for a none return value (tag exists but has no value)
	if value is None:
		print "    TAG NOT FOUND  " + lookupString
		value = ""

	return value

##
## Returns the Element where testfield = ID
##	Add full stop to go down a level ie. oompPart.oompID
def TPGEgetElementWhere(id, tree, testField):
	returnValue = ""

	xmlLookup = testField.split(".")
	running = True
	print len(xmlLookup)
	for x in range(0,len(xmlLookup)-1):
			try:
				#try and find the text if not found try and go down one step
				value = tree.findall(xmlLookup[x])
			except AttributeError:
				print "     XML TAG NOT FOUND " + testField + "  --  " + xmlLookup[x]
				value = ""
	for item in value:
		testValue = item.find(xmlLookup[len(xmlLookup)-1])
		if testValue.text == id:
			print "MATCH FOUND"
			returnValue = item

	return returnValue

##
## Get a list of all files with a filename iterating through the directory structure
##
def TPGEgetAllFilesIterate(directory, extension):
	returnValue = []

	import os
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.endswith(extension):
				returnValue.append(root + "\\" + file)


	return returnValue

##
## Returns resultField where testField = id in tree
##
def TPGEgetValueWhere(id, tree, testField, resultField):

	result = TPGEgetElementWhere(id, tree, testField)
	return TPGEgetValue(resultField, result)





#TESTING