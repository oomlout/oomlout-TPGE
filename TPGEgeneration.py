from TPGExml import TPGEgetValueExtra
from TPGExml import TPGEgetValue
from TPGExml import TPGEgetValueWhere
from TPGExml import TPGEgetValueIndex

import sys
import time
from TPGExml import TPGEgetAllFilesIterate

import xml.etree.ElementTree as ET
import os.path

templateFileName = "template/PROJ-template.tmpl"

tempPath = "tmp/"
tempCombinedXMLFileName = tempPath+"tempCombinedXML.xml"



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




# Main Routine
def TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML,template,output):
	print ("  TPGE -- Generating Pages")

	root = TPGEloadXML()

	#getting template name trying in ID directory
	##Need to ad a for each
	templateFileName = template
	try:
		templateFile = open(templateFileName,"r")
	except IOError:
		templateFileName = "template/TEST-template.tmpl"
		templateFile = open("template/TEST-template.tmpl","r")

	print "Using Template:  " + templateFileName

	outputFileName = output

	outputFile = open(outputFileName, "w+")


	#replaceTags
	for line in templateFile.readlines():
		line = TPGEreplaceLine(idString, line, root, baseDirectory)
		if line <> "":
			outputFile.write(line)
	outputFile.close()




def TPGEreplaceLine(idString, line, root, baseDirectory):
	includeLine = True

	##REPLACE ALL TAGS FIRST
	if includeLine:







		#####REPLACE TAGS
		#Replace all occurances of ID
		line = line.replace("%%ID%%", idString)

		if line[:1] == "#":
			#skip line
			r = 0
		else:
		######HANDLE LOOPING
		###^^0,12,%%U%%^^
			if find_between(line, "^^", "^^") != "":
				tag = find_between(line, "^^", "^^")
				print "Loop Tag Found: " + tag
				details = tag.split(",")
				frontBit=""
				backBit =""
				if '""' in line:
					splitString  = line[line.find("^^"):line.rfind('""')]
					line2 = splitString
					line2 = line2.replace('^^' + tag + '^^',"")
					frontBit = line[0:line.find("^^")]
					backBit = line[line.rfind('""')+2:len(line)]
					#print "Front Bit: " + frontBit
					#print "Line 2 " + line2
					#print "RESULTING STRING " + line2
					sys.stdout.write('.')
				else:
					splitString  = line.rpartition("^^" + tag + '^^')
					line2 = splitString[2]
					frontBit = splitString[0]
					#print "RESULTING STRING " + line2
					sys.stdout.write('.')
				line = ""   #reset line to nil
				for b in range(int(details[0]),int(details[1])+1):
					line3 = line2.replace(details[2],str(b))
					result = TPGEreplaceLine(idString,line3,root, baseDirectory)
					if result <> "":
						line = line + result
				line = frontBit + line + backBit #Re add front bit

			####### COMPLEX TAGS WITH INDEX
			while find_between(line, "!!", "!!") != "":
				#find first tag
				tag = find_between(line, "!!", "!!")
				#print "Tag = " + tag
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				value = TPGEgetValueIndex(details[0], root, details[1], details[2])
				#print "Replacing Tag Index:" + tag + "   " + value[0:20]
				line = line.replace("!!" + tag + "!!", value,1)
			for g in range(1,9):
				while find_between(line, "@" + str(g), "@" + str(g)) != "":
					#find first tag
					tag = find_between(line, "@" + str(g), "@" + str(g))
					details = tag.split(",")
					#TPGEgetValueWhere(id, tree, testField, resultField)
					#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
					#@@oompPart.oompID,name@@
					value = TPGEgetValueWhere(details[0], root, details[1], details[2])
					#print "Replacing Tag " + tag + "   " + value[0:20]
					line = line.replace("@" + str(g) + tag + "@" + str(g), value,1)
			while find_between(line, "@@", "@@") != "":
				#find first tag
				tag = find_between(line, "@@", "@@")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				value = TPGEgetValueWhere(details[0], root, details[1], details[2])
				#print "Replacing Tag " + tag + "   " + value[0:20]
				line = line.replace("@@" + tag + "@@", value,1)
			while find_between(line, "<<", "<<") != "":
				#find first tag
				tag = find_between(line, "<<", "<<")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				replaceValue = ""
				if details[0] == details[1]:
					replaceValue = details[2]
				line = line.replace("<<" + tag + "<<", replaceValue,1)

	includeLine = True
	##AFTER REPLACMENT TEST FOR INCLUSION
	if line[:1] == "#":
		#skip line as template comment
		print"Skipping Line   COMMENT    " + line[0:20]
		includeLine = False
	elif line[:1] == "$":
		#Test for file existance id directory based
		testFile =find_between(line, "$$", "$$")
		line = line.replace("$$" + testFile + "$$", "")
		#print "Testing File: " + baseDirectory + testFile
		if os.path.isfile(baseDirectory + testFile):
			#includeLine = True
			f=0
		else:
			#print"Skipping Line   FILE DOESN'T EXIST    " + line[0:20]
			includeLine = False
	elif line[:1] == "*":
		#Test for tag existance
		#find first tag
		tag = find_between(line, "**", "**")
		details = tag.split(",")
		#TPGEgetValueWhere(id, tree, testField, resultField)
		#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
		#@@oompPart.oompID,name@@
		#print tag
		try:
			value = TPGEgetValueWhere(details[0], root, details[1], details[2])
		except IndexError:
			print "ERROR IN LINE: " + tag + "LINE: " + line
			raise IndexError
		#print "Replacing Tag " + tag + "   " + value[0:20]
		line = line.replace("**" + tag + "**", "",1)
		if value <> "":
			line = line.replace("**" + tag + "**", "")
			#includeLine = True
		else:
			#print"      Skipping Line   TAG DOESN'T EXIST    " + line[0:20]
			includeLine = False
	elif line[:1] == "=":
		#Test for tag existance
		#find first tag
		tag = find_between(line, "==", "==")
		details = tag.split(",")
		#TPGEgetValueWhere(id, tree, testField, resultField)
		#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
		#@@oompPart.oompID,name@@
		#print tag
		try:
			value = TPGEgetValueIndex(details[0], root, details[1], details[2])
		except IndexError:
			print "ERROR IN LINE: " + tag + "LINE: " + line
			raise IndexError
		#print "Replacing Tag " + tag + "   " + value[0:20]
		line = line.replace("==" + tag + "==", "",1)
		if value <> "":
			line = line.replace("==" + tag + "==", "")
			#includeLine = True
		else:
			#print"      Skipping Line   TAG DOESN'T EXIST    " + line[0:20]
			includeLine = False
	elif find_between(line, "++", "++") != "":
		while find_between(line, "++", "++") != "":
				#find first tag
				tag = find_between(line, "++", "++")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				#print "Testing Equal: " +details[0] + "  " + details[1]
				if details[0] != details[1]:
					#print "      EXCLUDING"
					includeLine=False

				line = line.replace("++" + tag + "++", "")
	elif find_between(line, "??", "??") != "":
		while find_between(line, "??", "??") != "":
				#find first tag
				tag = find_between(line, "??", "??")
				#print "Tag = " + tag
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				#print "Testing Equal: " +details[0] + "  " + details[1]
				if details[0] == "inFamily":

					#print "Details " + details[1] + "  " + details[2]
					noneCount=0

					#testingType
					extraItem = "Type"
					partTest = TPGEgetValueWhere(details[1], root, "oompPart.oompID", "oomp"+ extraItem)
					familyTest = TPGEgetValueWhere(details[2], root, "oompFamily.familyName","family"+ extraItem)
					if familyTest <> "":
						if partTest != familyTest:
							includeLine = False
					else:
						noneCount += 1

					#testingSize
					extraItem = "Size"
					partTest = TPGEgetValueWhere(details[1], root, "oompPart.oompID", "oomp"+ extraItem)
					familyTest = TPGEgetValueWhere(details[2], root, "oompFamily.familyName","family"+ extraItem)
					if familyTest <> "":
						if partTest != familyTest:
							includeLine = False
					else:
						noneCount += 1

					#testingColor
					extraItem = "Color"
					partTest = TPGEgetValueWhere(details[1], root, "oompPart.oompID", "oomp"+ extraItem)
					familyTest = TPGEgetValueWhere(details[2], root, "oompFamily.familyName","family"+ extraItem)
					if familyTest <> "":
						if partTest != familyTest:
							includeLine = False
					else:
						noneCount += 1

					#testingDesc
					extraItem = "Desc"
					partTest = TPGEgetValueWhere(details[1], root, "oompPart.oompID", "oomp"+ extraItem)
					familyTest = TPGEgetValueWhere(details[2], root, "oompFamily.familyName","family"+ extraItem)
					if familyTest <> "":
						if partTest != familyTest:
							includeLine = False
					else:
						noneCount += 1

					#testingIndex
					extraItem = "Index"
					partTest = TPGEgetValueWhere(details[1], root, "oompPart.oompID", "oomp"+ extraItem)
					familyTest = TPGEgetValueWhere(details[2], root, "oompFamily.familyName","family"+ extraItem)
					if familyTest <> "":
						if partTest != familyTest:
							includeLine = False
					else:
						noneCount += 1


					if noneCount > 1:
						includeLine = False


				line = line.replace("??" + tag + "??", "")
	#special tests
	else:
		r=7
	if includeLine:
		return line
	else:
		return ""










def TPGEcreateXMLList(list):
	xmlFiles = list

	try:
		os.stat(tempPath)
	except:
		os.mkdir(tempPath)

	f = open(tempCombinedXMLFileName,'w+')
	f.write("<xml>")

	print "---------"
	for item in xmlFiles:
		if item <> "":
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

def TPGEcreateXML(idString, baseDirectory, xmlAdd, extraXML):

	xmlFileName = TPGEgetAllFilesIterate("tags/", ".xml")

	fileList = extraXML.split(",")

	moreXML = []

	for item in fileList:
		print "Loading XML Files From: " + item
		if os.path.isdir(item):
			moreXML = moreXML + TPGEgetAllFilesIterate(item, xmlAdd)
		else:
			moreXML.append(item)
	moreXML = moreXML + xmlFileName

	TPGEcreateXMLList(moreXML)


def TPGEloadXML():
	tree = ET.parse(tempCombinedXMLFileName)
	return tree.getroot()


