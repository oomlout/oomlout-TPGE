oomlout-TPGE
============

TPGE -- Generating pages from template files in python

#COMMAND LINE


-A or -ALL		Generate all OOMP Pages

TPGEmain.py IDstring baseDirectory xmlAddition extra xml

IDSTring		--	The ID of the part being dealt with
baseDirectory	--	BaseDirectory
xmlAddition		--	The XML info file in baseDirectory/IDString-xmlAddition
extraXML 		--  Extra xmlFile to load (need to upgrade to be a list) 

# Tag Types

((In order of execution))

'## -- Marks line as a comment
'%% -- Replace with program variable (ie. ID)
^^0,12,%%U%%^^ -- Process the following line for a range 0 to 12 replacing %%U%% with the variable

'!! -- Complex tag format index			@@INDEX,tag to match,name of tag to return@@		!!1,oompPart.oompID,name!! -- Returns first name of first oompPart
'@1-@9 Priority tag processing 1 first 9 last same as below
'@@ -- Complex tag format 				@@ID,tag to match,name of tag to return@@		@@%%ID%%,oompPart.oompID,name@@


# Filter Types
		--NO spaces between these important first charachter
'$$ -- Test for file existing if it does process line file between %%FILENAME%% referenced on base directory
'** -- Test if a tag value exists

# XML Files to load

'BASE FILE --- /tags/


# File Descriptions

'TPGEmain.py		-- The main command line program
'TPGEgeneration.py	-- Used for generating files
'TPGExml.py			-- XML support routines


# Process

TPGELoadXML(idString, baseDirectory, xmlAdd, extraXML)
	
	