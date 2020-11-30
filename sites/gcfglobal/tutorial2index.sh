#!/bin/bash 
for f in $(find .|grep tutorial.html); do
  fnew=`echo $f | sed 's/_h.png/_half.png/'`
  echo mv $fnew $(dirname $f)/index.html
  mv $fnew $(dirname $f)/index.html
done
