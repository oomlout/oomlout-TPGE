oomlout-TPGE
============

TPGE -- Generating pages from template files in python

#COMMAND LINE

TPGEmain.py IDstring baseDirectory xmlAddition extra xml

IDSTring		--	The ID of the part being dealt with
baseDirectory	--	BaseDirectory
xmlAddition		--	The XML info file in baseDirectory/IDString-xmlAddition
extraXML 		--  Extra xmlFile to load (need to upgrade to be a list) 

# Tag Types

'## -- Marks line as a comment
'%% -- Replace with program variable (ie. ID)
'@@ -- Simple Tag
'!! -- Complex tag format !!oompTag.tagName=VALUE=oompTag.tagType!! (returns tagType for the tag where tagName = VALUE


# Filter Types

'^^ -- Test for file existing if it does process line file between %%FILENAME%% referenced on base directory
'** -- Test if a tag value exists

# XML Files to load

'BASE FILE --- /tags/


# File Descriptions

'TPGEmain.py		-- The main command line program
'TPGEgeneration.py	-- Used for generating files
'TPGExml.py			-- XML support routines