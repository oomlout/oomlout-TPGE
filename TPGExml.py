
import xml.etree.ElementTree as ET

xmlFileName = "tags/TPGE-oomlout-tags.xml"

xmlIDBase = "c:/GH/oomlout-"

def TPGEloadXML():
	tree = ET.parse(xmlFileName)
	root = tree.getroot()
	return root

def TPGEloadIDXML(idString):
	xmlIDFileName = xmlIDBase + idString + "/" + idString + "-xml.xml"
	tree = ET.parse(xmlIDFileName)
	root = tree.getroot()
	return root



def TPGEgetValue(lookupString, tree):
	xmlLookup = lookupString.split(".")
	for tag in xmlLookup:
		try:
			value = tree.find(tag).text
		except AttributeError:
			print "TAG NOT FOUND " + tag
			value = ""
		try:
			tree = tree.find(tag)
		except AttributeError:
			print "TAG NOT FOUND 2  " + tag
			value = ""

	return value



#TESTING
TPGEloadXML()
