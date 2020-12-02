#!/bin/bash -x
# The scraping of gcfglobal can be simplified with wget fix links
DISPDIR=/library/www/html/modules/oneline

#wget -nHc -r -P $DISPDIR/ -k -K --page-requisites https://edu.gcfglobal.org/
   

wget -nHc -r --level=10  -I es -P $DISPDIR/ -k -K --page-requisites https://edu.gcfglobal.org/
