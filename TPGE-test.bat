@echo off
set WIKBdirectory=C:\GH\oomlout-WIKB\
set TPGEdirectory=C:\GH\oomlout-TPGE\

echo on

REM
REM 	Creating Test
REM

python %TPGEdirectory%TPGEmain.py -id CRHO-I01-B-02PI-01 -bd C:\KB\oomp-scripts\oomp-gen\parts\ -xa .oomp -ex C:\KB\oomp-scripts\oomp-gen\parts\ -tm C:\GH\oomlout-TPGE\template/TEST-template.tmpl.html -of C:\GH\oomlout-TPGE\tmp\TEST.html


