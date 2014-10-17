import pywikibot, os, time
site = pywikibot.Site('en', 'oomlout')  # The site we want to run our bot on



def WIKIuploadAllOOMP(baseDirectory):
	print "Generating All OOMP Files:"

	for x in os.walk(baseDirectory):
		idString = str(x[0].replace(baseDirectory, ""))
		print "     Uploading ---> " + idString
		if idString <> "" :
			page = pywikibot.Page(site, 'oomp/part/' + idString)
			oompFileName = baseDirectory + idString + "/" + idString + ".html"
			# print "FileName:  " + oompFileName
			oompFile = open(oompFileName)
			oompFileContents = oompFile.read()
			page.text = oompFileContents
			page.save('Updating File - ' + time.strftime("%d/%m/%Y %H:%M:%S"))  # Saves the page


baseDirectory = "C:/KB/oomp-scripts/oomp-gen/parts/"

WIKIuploadAllOOMP(baseDirectory)