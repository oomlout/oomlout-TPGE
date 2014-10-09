from TPGExml import TPGEgetValueExtra
from TPGExml import TPGEgetValue
from TPGExml import XMLCombiner



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

	TPGELoadXML(idString, baseDirectory, xmlAdd, extraXML)
	tree = ET.parse(tempCombinedXMLFileName)
	root = tree.getroot()


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
			templateFile = open("template/OOMP-template.tmpl","r")


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
				value = TPGEgetValue(tag, root)

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
	xmlFileName = "tags/TPGE-oomlout-tags.xml"
	xmlIDFile = baseDirectory + "/" + idString + xmlAdd
	moreXML = extraXML.split(",")
	moreXML.append(xmlFileName)
	moreXML.append(xmlIDFile)

	xmlFiles = (moreXML)

	print ("Loading XML FILES:  ")
	for item in xmlFiles:
		print "    " + item
	print "---------"

	r = XMLCombiner(xmlFiles).combine()
	f = open(tempCombinedXMLFileName,'w+')
	f.write(r)
	f.close()



TPGEgeneratePages("LEDS-10-L-FROS-01", "C:/GH/oomp-scripts/oomp-gen/parts/LEDS-10-L-FROS-01/", ".oomp", "tags/OOMP-oomlout-tags.xml,tags/oomp-Tag-Details-NEW.oomp")
