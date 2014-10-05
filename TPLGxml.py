
import xml.etree.ElementTree as ET

xmlFileName = "xml/testXML.oomp"

def TPGEloadXML():
	tree = ET.parse(xmlFileName)
	root = tree.getroot()

	return root



def TPGEgetValue(lookupString, tree):
	xmlLookup = lookupString.split(".")
	for tag in xmlLookup:
		value = tree.find(tag).text
		tree = tree.find(tag)

	return value



#TESTING
TPGEloadXML()
