from TPGExml import TPGEgetValueExtra
from TPGExml import TPGEgetValue
from TPGExml import TPGEgetValueWhere
from TPGExml import TPGEgetValueIndex
from random import randint

import codecs
import sys
import time
from datetime import date,datetime
from TPGExml import TPGEgetAllFilesIterate

import xml.etree.ElementTree as ET
import os.path

templateFileName = "template/PROJ-template.tmpl"



tempPath = "tmp/"
tempCombinedXMLFileName = tempPath + str(randint(0,999999)) + "tempCombinedXML.xml"



def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""




# Main Routine
def TPGEgeneratePages(idString, baseDirectory, xmlAdd, extraXML,template,output, root):
	#print ("  TPGE -- Generating Pages")
	
	done = False
	
	

	#getting template name trying in ID directory
	##Need to ad a for each
	templateFileName = template
	try:
		templateFile = open(templateFileName,"r")
	except IOError:
		print "Can't find template: " + templateFileName
		templateFileName = "template/TEST-template.tmpl"
		templateFile = open("template/TEST-template.tmpl","r+")

	#print "Using Template:  " + templateFileName

	output = TPGEreplaceLine(idString, output, root, baseDirectory)

	outputFileName = output
	path = os.path.dirname(outputFileName)
	print "Path: " + path
	if not os.path.exists(path):
		os.makedirs(path)
	outputFile = open(outputFileName, "w+")


	#replaceTags
	runLine = ""

	running = False
	for line in templateFile.readlines():




		#test for multiline entry
		if line.startswith("::::",0,4) or running == True:
			#print "    ML    " + line
			running = True
			if running:
				if line.startswith(";;;;",0,4):
					
					line = TPGEreplaceLine(idString, runLine, root, baseDirectory)
					runLine = ""
					running = False
					#print "   FINISHED MULTILINE"
					line = line.replace("::::","")
					line = line.replace(";;;;","")
					line = line.rstrip()
					line = line.lstrip()
					line = line + "\n"
					if line <> "":
						outputFile.write(line.encode('utf8'))
				else:
					#print "    Adding to line"
					line = line.replace("\n","")
					line = line.replace("\r","")
					runLine = runLine + line
		else:
			#print "    RL" + line + "()"
			runLine = line
			line = TPGEreplaceLine(idString, runLine, root, baseDirectory)
			runLine = ""
			if line <> "":
				#print "----" + line + ">>>>>>"
				if "%$%DELETE FILE%$%" in line:
					outputFile.close()
					os.remove(outputFileName)
					print "   +++++++++++++++++++++NOT CREATING FILE DUE TO TEST++++++++++++++++++++++++++++++"
					done = True
					break
				else:
					outputFile.write(line.encode('utf8'))
			if done:
				break
		if done:
			break
	outputFile.close()
	




def TPGEreplaceLine(idString, line, root, baseDirectory):
	includeLine = True

	##REPLACE ALL TAGS FIRST
	if includeLine:







		#####REPLACE TAGS
		#Replace all occurances of ID
		####MAGIC WORDS
		line = line.replace("%%ID%%", idString)
		line = line.replace("%%YEAR%%", str(date.today().year).zfill(2))
		line = line.replace("%%MONTH%%", str(date.today().month).zfill(2))
		line = line.replace("%%DAY%%", str(date.today().day).zfill(2))
		line = line.replace("%%HOUR%%", str(datetime.now().hour).zfill(2))
		line = line.replace("%%MINUTE%%", str(datetime.now().minute).zfill(2))
		


		if line[:1] == "#":
			#skip line
			r = 0
		else:
		######HANDLE LOOPING
		###^^0,12,%%U%%^^
			if find_between(line, "^^", "^^") != "":
				tag = find_between(line, "^^", "^^")
				#print "Loop Tag Found: " + tag
				details = tag.split(",")
				frontBit=""
				backBit =""
				if '""' in line:
					splitString  = line[line.find("^^"):line.rfind('""')]
					line2 = splitString
					line2 = line2.replace('^^' + tag + '^^',"")
					#print line2
					frontBit = line[0:line.find("^^")]
					backBit = line[line.rfind('""')+2:len(line)]
					#print "Front Bit: " + frontBit
					#print "Line 2 " + line2
					#print "RESULTING STRING " + line2
					#sys.stdout.write('.')
				else:
					splitString  = line.rpartition("^^" + tag + '^^')
					line2 = splitString[2]
					frontBit = splitString[0]
					#print "RESULTING STRING " + line2
					#sys.stdout.write('.')
				line = ""   #reset line to nil
				try:
					for b in range(int(details[0]),int(details[1])+1):
						#print b
						#sys.stdout.write('.')
						#print "Looping: " + str(b)
						line3 = line2.replace(details[2],str(b))
						result = TPGEreplaceLine(idString,line3,root, baseDirectory)
						#print result
						if result <> "" and result <> "\n":
							line = line + result
						includeLine = True
				except:
					print "Problem with line: " + line2
				line = frontBit + line + TPGEreplaceLine(idString,backBit,root, baseDirectory) #Re add front bit
				
				#print ""

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

				#print "Details:  "
				#print "  Tag:" +  tag
				#print "  D1" + details[0]
				#print "  D2" + details[1]
				#print "  D3" + details[2]

				value = TPGEgetValueWhere(details[0], root, details[1], details[2])
				#print "Replacing Tag " + tag + "   " + value[0:20]
				line = line.replace("@@" + tag + "@@", value,1)
			while find_between(line, "''", "''") != "":
				tag = find_between(line, "''", "''")
				details = tag.split(",")
				if os.path.isfile(baseDirectory + details[0]):
					value = details[1]
				else:
					try:
						value = details[2]
					except:
						value = ""
				line = line.replace("''" + tag + "''", value,1)
			while find_between(line, "()", "()") != "":
				#find first tag
				tag = find_between(line, "()", "()")
				details = tag.split(",")
				#print "TESTING FOR CREATION: " +  details[0] + "  " + details[1]
				if details[0] != details[1]:
					replaceValue = "%$%DELETE FILE%$%"
				else:
					replaceValue = ""
				line = line.replace("()" + tag + "()", replaceValue,1)	
				#print line
			while find_between(line, "!)", "!)") != "":
				#find first tag
				tag = find_between(line, "!)", "!)")
				details = tag.split(",")
				details = tag.split(",")
				details = tag.split(",")
				#print "TESTING FOR CREATION: " +  details[0] + "  " + details[1]
				if details[0] == details[1]:
					replaceValue = "%$%DELETE FILE%$%"
				else:
					replaceValue = ""
				line = line.replace("!)" + tag + "!)", replaceValue,1)	
				#print line
			while find_between(line, "(*", "(*") != "":
				#find first tag
				tag = find_between(line, "(*", "(*")
				details = tag.split(",")
				
				if os.path.isfile(baseDirectory + details[0]):
					replaceValue = details[1]
				else:
					replaceValue = details[2]
				line = line.replace("(*" + tag + "(*", replaceValue,1)	
				#print line				
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
				else:
					try:
						replaceValue = details[3]
					except:
						replaceValue = ""
				
				line = line.replace("<<" + tag + "<<", replaceValue,1)
			while find_between(line, ">>", ">>") != "":
				#find first tag
				tag = find_between(line, ">>", ">>")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				replaceValue = ""
				if details[0] != details[1]:
					replaceValue = details[2]
				line = line.replace(">>" + tag + ">>", replaceValue,1)

			
	includeLine = True
	##AFTER REPLACMENT TEST FOR INCLUSION
	if line[:1] == "#":
		#skip line as template comment
		#print"Skipping Line   COMMENT    " + line[0:20]
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
			#print"     Skipping Line   FILE DOESN'T EXIST    " + line[0:20]
			includeLine = False
	elif find_between(line, "**", "**") != "":
		while find_between(line, "**", "**") != "":

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
				#print "Skipping Due To **   " + tag
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
			#print "Replacing Tag " + tag + "   " + value[0:20]
			line = line.replace("==" + tag + "==", "",1)
			if value <> "":
				line = line.replace("==" + tag + "==", "")
				#includeLine = True
			else:
				#print"      Skipping Line   TAG DOESN'T EXIST    " + line[0:20]
				includeLine = False
		except IndexError:
			pass
			#print "ERROR IN LINE: Bypassed for wiki formatting" + tag
			#raise IndexError
			#added to allow for WIKImedia style formating
	elif find_between(line, "++", "++") != "":
		while find_between(line, "++", "++") != "":
				#find first tag
				tag = find_between(line, "++", "++")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				#@@oompPart.oompID,name@@
				#print "Testing Equal: " +details[0] + "  " + details[1]
				
				if details[0] != details[1]:
					#print "      EXCLUDING"
					includeLine=False
					#print "Skipping Due To ++   " + tag
				line = line.replace("++" + tag + "++", "")
	elif find_between(line, "--", "--") != "":
		while find_between(line, "--", "--") != "":
				#find first tag
				tag = find_between(line, "--", "--")
				details = tag.split(",")
				#TPGEgetValueWhere(id, tree, testField, resultField)
				#TPGEgetValueWhere("BOLT-M3-M-12-01", root, "oompPart.oompID", "name")
				#@@oompPart.oompID,name@@
				#print "Testing Equal: " +details[0] + "  " + details[1]
				try:
					#was killing one so fixed
					if details[0] == details[1]:
						#print "      EXCLUDING"
						includeLine=False
						#print "Skipping Due To --"
					line = line.replace("--" + tag + "--", "")
				except IndexError:
					line = line.replace("--" + tag + "--", "")
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
		##Add new line's

		line = line.replace("~~", "\n")

				####MAGIC WORDS
		line = line.replace("%%ID%%", idString)
		line = line.replace("%%YEAR%%", str(date.today().year).zfill(2))
		line = line.replace("%%MONTH%%", str(date.today().month).zfill(2))
		line = line.replace("%%DAY%%", str(date.today().day).zfill(2))
		line = line.replace("%%HOUR%%", str(datetime.now().hour).zfill(2))
		line = line.replace("%%MINUTE%%", str(datetime.now().minute).zfill(2))
		line = line.replace("%%CRLF%%", "\n")

		#print "BOTTOM  " + line
		
		return line
	else:
		return ""










def TPGEcreateXMLList(list, baseDirectory):

	
	xmlFiles = list

	try:
		os.stat(tempPath)
	except:
		os.mkdir(tempPath)

	f = codecs.open(tempCombinedXMLFileName,'w+', encoding='utf-8')
	f.write("<xml>".encode('utf-8'))

	print "---------"
	for item in xmlFiles:
		if item <> "":
			for line in open(item):
				if ("<xml>" in line) or ("</xml>" in line):
					t = 0
			#		sys.stdout.write("S")
				else:
					value = unicode(line, 'utf-8', errors='ignore')
					f.write(value)
			#		sys.stdout.write(".")
			#print ""
	f.write("</xml>".encode('utf-8'))
	f.close()

def TPGEcreateXML(idString, baseDirectory, xmlAdd, extraXML):

	if extraXML != "":
		extraXML = extraXML + "," + baseDirectory
	else:
		extraXML = baseDirectory + ","

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



	TPGEcreateXMLList(moreXML, baseDirectory)


def TPGEloadXML():
	print "Loading XML"
	tree = ET.parse(tempCombinedXMLFileName)
	print "Done Loading XML"
	return tree.getroot()


