#!/bin/bash

control_c()
{
  echo "Bye bye"
  exit 1
}

i="0"
while [ $i -lt 3 ]
do
  date
  trap control_c SIGINT
done


