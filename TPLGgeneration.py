
from TPGExml import TPGEloadXML
from TPGExml import TPGEloadGetValue


templateFileName = "template/test.html"
tagFileName = "tags/testTags.txt"
outputFileName = "output/testOutput.html"
tempFileName = "output/temp.html"


def TPGEloadTags():
	tagFile = open(tagFileName)

	returnArray = []

	for line in tagFile.readlines():
		if line[:0] == "#":
			print "COMMENT -->  "  + line
			#skip as comment
		elif ',' in line:
			print "TAG -->  " + line
			returnArray.append(line.split(","))
		else:
			print "."
			#skip as empty


	return returnArray







def TPGEgeneratePages():
	print ("  TPGE -- Generating Pages")

	# Read Template File
	templateFile = open(templateFileName,"r")

	tempFile = open(tempFileName)

	tags = TPGEloadTags()

	#replaceTags
	for line in templateFile.readlines():



		if line[:0] == "#":
			#skip line as template comment
			print"."
		for tag in tags:
			newLine = line.replace("@@" + tag[0] + "@@", tag[1])
			tempFile.write(newLine)

	tempFile.close()

	templateFile = open(tempFileName,"r")


	#REPLACE SIMPLE TAGS

	#open templateFile
	outputFile = open(outputFileName,"w+")




	for line in templateFile.readlines():
		if line[:0] == "#":
			#skip line as template comment
			print"."
		for tag in tags:
			newLine = line.replace("@@" + tag[0] + "@@", tag[1])
			outputFile.write(newLine)





	print templateFile.read()







