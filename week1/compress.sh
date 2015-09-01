#!/bin/bash
# $1 = directory to search for files
# $2 = minimum file size in kilobytes

#declare -i i # C-style for-loop
#for ((i=0; i<$n; i++)); do
#   echo $c
#done


find ~/Desktop/testdirectory/ -size +200k -exec gzip


find $HOME -name '*' -type f -size +2000 -exec ls -s {} \; -exec rm -f {} \;

