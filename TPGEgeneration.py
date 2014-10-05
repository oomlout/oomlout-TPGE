
from TPGExml import TPGEloadXML
from TPGExml import TPGEloadIDXML
from TPGExml import TPGEgetValue


templateFileName = "template/PROJ-template.tmpl"
tagFileName = "tags/TPGE-oomlout-tags.xml"
outputFileName = "output/testOutput.html"
tempFileName = "output/temp.html"




def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""


# Main Routine
def TPGEgeneratePages(idString):

	xmlIDBase = "c:/GH/oomlout-"
	idDirectory = xmlIDBase + idString + "/"

	print ("  TPGE -- Generating Pages")

	#load xml tree
	#maybe redefine filenames here
	root = TPGEloadXML()
	root2 = TPGEloadIDXML(idString)

	#getting template name trying in ID directory
	##Need to ad a for each
	templateFileName = idDirectory + TPGEgetValue("basics.template", root2)
	try:
		templateFile = open(templateFileName,"r")
	except IOError:
		templateFileName = TPGEgetValue("basics.template", root2)
		templateFile = open("template/" + templateFileName,"r")


	outputFile = open(idDirectory + TPGEgetValue("basics.output", root2), "w+")


	#replaceTags
	for line in templateFile.readlines():
		if line[:1] == "#":
			#skip line as template comment
			print"Skipping Line   " + line
		else:
			#Replace all occurances of ID
			line = line.replace("%%ID%%", idString)

			while find_between(line, "@@", "@@") != "":
				#find first tag
				tag = find_between(line, "@@", "@@")
				value = TPGEgetValue(tag, root)
				if value == "":
					#If not in base tag file try ID tag file
					value = TPGEgetValue(tag, root2)

				print "Replacing Tag " + tag + "   " + value
				line = line.replace("@@" + tag + "@@", value)
			outputFile.write(line)

	outputFile.close()

