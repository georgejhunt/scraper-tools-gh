#!/bin/bash -x
# The scrapint of gcfglobal may be easy enough to do in bash

WORKDIR=/library/working/rachel/gcf
mkdir -p $WORKDIR/zip-files

# Get the current download page which has the names o the zip files
if [ ! -f $WORKDIR/download-all.html ];then
   wget -O $WORKDIR/download-all.html https://edu.gcfglobal.org/en/download/all
fi


# make a list of URL's for downloading
grep .*\.zip $WORKDIR/download-all.html | cut -f6 -d'"' >$WORKDIR/ziplist

# If the zip files are not preent, get them
for f in $(cat $WORKDIR/ziplist);do
   if [ ! -f $WORKDIR/zip-files/$(basename $f) ];then
      echo Looking for $WORKDIR/zip-file/$(basename $f)
      wget -P $WORKDIR/zip-files $f
   else
      echo Already downloaded $f
   fi
done

# Unzip the conten to a place where they can be displayed
DISPDIR=/library/www/html/modules/en-gcfglobal_2020
mkdir -p $DISPDIR

curdir=$(pwd)
for f in $(cat $WORKDIR/ziplist);do
   basename=$(basename $f)
   base=${basename%.zip}
   if [ ! -d $DISPDIR/$base ];then
      mkdir -p $DISPDIR/$base
      cd $DISPDIR/$base/
      echo $DISPDIR/$base
      /usr/bin/unzip -q $WORKDIR/zip-files/$basename
   fi
done
cd $curdir

# get the topic director from the live site which has all the menus
   wget -nH -r -P $DISPDIR/ -I en/topics https://edu.gcfglobal.org/



