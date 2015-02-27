# oomlout-TPGE
A command line python tool used for generating pages from template files, being fed by xml.

## Command Line Parameters

* -id				-- id String
* -bd				-- baseDirectory
* -xo				-- xmlOutut - name of output file with directory
* -xa				-- xmlAddition extension for your xml files (default .xml)
* -ex				-- extraXml list of directories or files to harvest xml data from
* -rm				-- runMode for doing special things (A,ALL generate all)
* -tm 				-- template name
* -ui				-- unique ID name (make a page for each element in this)


## Tag Types

((In order of execution))

### Control Tags

|Tag Marker			|	Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| ## 				|	Marks line as a comment																|	##A Comment
| ::::	- ;;;;		|	Multi line statement start with this and only this and end with it as well
| %% 				|	Replace with program variable (ie. ID)												|	%%ID%%	(currently only ID supported, plans to add date etc.)
| ~~				| 	Replace with new line charachter													| 	~~
| ^^ ("" end bracket)|	Process the following line for a range 0 to 12 replacing %%U%% with the variable	|	^^0,12,%%U%%^^CONTENT TO PROCESS""  (loop from 0 to 12, replacing the tag %%U%% in the current line, can be used recursively but some care is needed. Everything to the right of this loop tag is processed with it) ("" used to bracket effective area so to allow adding things at the end rather than every cycle)

### Magic Words

|Word				| Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| %%ID%%			|	Page ID sent from command line														|	BREB-01
| %%YEAR%%			|	Current Year														|	2014
| %%MONTH%%			|	Current Month														|	08
| %%DAY%%			|	Current Day														|	05
| %%HOUR%%			|	Current Hour														|	09
| %%MINUTE%			|	Current Minute														|	45
 


### Replacing Tags Based On XML

|Tag Marker			|	Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| !!				| Complex tag format index																|	!!1,oompPart.oompID,name!! -- Returns first name of first oompPart
| @1-@9				| Priority tag processing 1 first 9 last same as below									|
| @@ 				| Complex tag format	(add &&#&& to get index of an item ie.&&2&& second occurrence)	|															|	@@ID,tag to match,name of tag to return@@		@@%%ID%%,oompPart.oompID,name@@<br> Example for items out of a list<br>@@%%ID%%,oomloutPart.oomID,partsList.partEntry.qty&&%%Y%%&&@@
| ''				| Test for file																			|   ''f.jpg,if exists, if doesn't'' 						


### Inclusion Test Tags

-- NO spaces between these important first charachter (the case for some but not others)

|Tag Marker			|	Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| ()				| First line in file test to see if file is created, If the value matches the second value then create | ()@@ID,tag to match,name of tag to return@@()
| !)				| First line in file test to see if file is created, If the value matches the second value then create | !)@@ID,tag to match,name of tag to return@@!)
| $$ 				| Test for file existing if it does process line file between %%FILENAME%% referenced on base directory | $$%%ID%%.jpg	|
| (*				| Test for file if it exists include first bit otherwise second bit						|	()FILE,INCLUDE,INCLUDE IF NOT EXISTING()		
| ** 				| Test if a tag value exists															|	\*\*ID,tag to match,name of tag to return\*\*(TEST value for  @@ above TODO-make a wrapper to use @@)
| == 				| Test if a tag exists (index linked)													|	==1,oompPart.oompID,name== (TEST value for  !! above TODO-make a wrapper to use !!)
| ++ 				| Include if two values are the same (whole Line)										|	++CRHO,CRHO++ ++@@%%ID%%,oompPart.oompID,hexID@@,AEA++
| -- 				| Include if two values are not the same (whole Line)
| <<				| Include tag (ie. value, value, include text)											|	<<CRHO,CRHO, text to include,(optional)include if not a match<<
| >>				| Include tag if not equal (ie. value, value, include text)		

### Special Types
|Tag Marker			|	Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| ?? 				| Marks a special inclusion test, first item is test type											| ??inFamily,ID,FamilyName??

SPECIAL TESTS
|Tag Marker			|	Description																			|	Example
|-------------------|---------------------------------------------------------------------------------------|-------------------------------|
| inFamily			| Whether an ID is in a family															| ??inFamily,ID,FamilyName??

	To Implement
	-Test if in family-
	-Unique item within family


## File Descriptions

* TPGEmain.py		-- The main command line program
* TPGEgeneration.py	-- Used for generating files
* TPGExml.py			-- XML support routines


## To Do List

* Add doesn't exist tag to ** tests and $$