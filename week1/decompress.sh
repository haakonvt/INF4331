#!/bin/bash

if [ "$2" != "" ] || [ "$1" = "" ]; then
   echo "Wrong number of arguments, only need one: path to directory"
   exit 1
fi
if [ "$1" = "-h" ] || [ "$1" = "-help" ]; then
   echo "Please input the path as first argument to the directory you want to look for files to decompress. I.e. ~/../MyFolder/"<&2
else
   gzip `find "$1" -name *.gz` -d
   exit 1
fi
