#!/bin/bash
x=$(echo $1 | bc -l)
echo "$1 = $x"
