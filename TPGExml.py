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
		#print "    TAG NOT FOUND  " + lookupString
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
		#print "    TAG NOT FOUND  " + lookupString
		value = ""

	return value




##
## Returns the Element where testfield = ID
##	Add full stop to go down a level ie. oompPart.oompID
def TPGEgetElementWhere(id, tree, testField):
	returnValue = ""

	xmlLookup = testField.split(".")
	running = True
	#print len(xmlLookup)
	for x in range(0,len(xmlLookup)-1):
			try:
				#try and find the text if not found try and go down one step
				value = tree.findall(xmlLookup[x])
			except AttributeError:
				#print "     XML TAG NOT FOUND " + testField + "  --  " + xmlLookup[x]
				value = ""
	for item in value:
		testValue = item.find(xmlLookup[len(xmlLookup)-1])
		try: 
			if testValue.text == id:
				#print "MATCH FOUND"
				returnValue = item
		except:
			pass
	return returnValue

##
## Get a list of all files with a filename iterating through the directory structure
##
def TPGEgetAllFilesIterate(directory, extension):
	returnValue = []

	import os
	for root, dirs, files in os.walk(directory):
		for file in files:
			if file.endswith(extension) or file.endswith(".xml"):
				returnValue.append(root + "\\" + file)


	return returnValue

##
## Returns resultField where testField = id in tree
##
def TPGEgetValueWhere(id, tree, testField, resultField):

	#print "TPGEgetValueWhere(id, tree, testField, resultField)" + id + " " + testField + " " + resultField

	if find_between(resultField, "&&", "&&") <> "":
		pass
	else:
		resultField = resultField + "&&0&&"

	index = find_between(resultField, "&&", "&&")
	resultField = resultField.replace("&&" + index + "&&", "")

	if index == "0":
		#out style first index remaining unchanged
		result = TPGEgetElementWhere(id, tree, testField)
		return TPGEgetValue(resultField, result)
	else:
		result = TPGEgetElementWhere(id, tree, testField)
		p = resultField.split(".")
		#needs fixing for more than 3 elements


		if len(p) == 3:
			testField = p[0]
			result = TPGEgetElementIndex(0, result, testField)
			returnValue = TPGEgetValueIndex(index, result, p[1], p[2])
		elif len(p) == 2:
			testField = p[0]
			#result = TPGEgetElementIndex(0, result, testField)
			print str(result.text) + "   " + p[0] +  "  " + p[1]

			returnValue = TPGEgetValueIndex(index, result, p[0], p[1])



			#returnValue =  TPGEgetValueIndex(index, result, "includesList.include", "include")
			#returnValue =  TPGEgetValueIndex(index, result, resultField, p[1])

		return returnValue
##
## Returns the Element where index = index
##	Add full stop to go down a level ie. oompPart.oompID
def TPGEgetElementIndex(index, tree, testField):
	returnValue = ""

	xmlLookup = testField.split(".")
	running = True

	#messy way to deal with length one issue (could be fixed)
	if len(xmlLookup) == 1:

		for x in range(0,len(xmlLookup)):
				try:
					#try and find the text if not found try and go down one step
					value = tree.findall(xmlLookup[x])
				except AttributeError:
					#print "     XML TAG NOT FOUND " + testField + "  --  " + xmlLookup[x]
					value = ""
		try:
			returnValue = value[int(index)]
		except IndexError:
			returnValue = ""

	else:

		for x in range(0,len(xmlLookup)-1):
				try:
					#try and find the text if not found try and go down one step
					value = tree.findall(xmlLookup[x])
				except AttributeError:
					#print "     XML TAG NOT FOUND " + testField + "  --  " + xmlLookup[x]
					value = ""
		try:
			returnValue = value[int(index)]
		except IndexError:
			returnValue = ""


	return returnValue

##
## Returns resultField for index item in testField
##
def TPGEgetValueIndex(index, tree, testField, resultField):

	result = TPGEgetElementIndex(index, tree, testField)

	return TPGEgetValue(resultField, result)

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""



#TESTING