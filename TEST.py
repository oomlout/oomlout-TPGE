from TPGExml import TPGEgetValueExtra
from TPGEgeneration import TPGELoadXMLList
from TPGExml import TPGEgetElementWhere
from TPGExml import TPGEgetValue
from TPGExml import TPGEgetAllFilesIterate
from TPGExml import TPGEgetValueWhere

#TPGELoadXML(idString, baseDirectory, xmlAdd, extraXML):

list = "C:\GH\oomp-scripts\oomp-gen\parts\LEDS-10-G-FROS-01\LEDS-10-G-FROS-01.oomp","C:\GH\oomp-scripts\oomp-gen\parts\oomp-Supplier-Details.oomp"



directory = "C:\GH\oomp-scripts\oomp-gen\parts"

oompList = TPGEgetAllFilesIterate(directory, ".oomp")


root = TPGELoadXMLList(oompList)

#~ #def TPGEgetValueExtra(lookupString, tree, testValue, returnValue)

#~ lookupString = "oompSupplier.supplierCode"
#~ root = root
#~ testValue = "oompColor"
#~ returnValue = "tagReadable"

#~ #print TPGEgetValueExtra(lookupString, root, testValue, returnValue)

id = "BOLT-M3-M-12-01"
tree = root
testField = "oompPart.oompID"

result = TPGEgetElementWhere(id, tree, testField)

resultField = "name"

print "Lookup --- " + TPGEgetValueWhere(id, tree, testField, resultField)

#~ print type(result)
#~ print result



#~ print ""
#~ print ""

#~ print root

#~ print root.items()

#~ result = root.findall("oompSupplier")

#~ print result

#~ for child in result:
	#~ t = child.find("supplierCode")
	#~ print child.tag, child.text

#~ #for child in root:
#~ #	print child.tag, child.attrib
