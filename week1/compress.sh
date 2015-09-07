#!/bin/bash

if [ "$1" = "-h" ] || [ "$1" = "-help" ]; then
   echo "Please input the path as first argument to the directory you want to look for files to compress. I.e. ~/../MyFolder/"
   exit 1
fi

if [ "$#" != "2" ]; then
   echo "Wrong number of arguments, only need two:"
   echo "1) path to directory"
   echo "2) file minimum size"
   exit 1
else
   gzip `find "$1" -size +"$2"k`
   exit 1
fi
