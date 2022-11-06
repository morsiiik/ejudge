#!/bin/bash

answers=(15 996 99556547 15 2000000000 15 15 333 19900080000 2672564083 15)
for ((i=1; i<12; i++))
do

time a=$(cat ./ainput/$i | python  $1)
if [[ $a -eq ${answers[$i-1]} ]]; then
    echo "test $i yes"
else
    echo "test $i no"
fi
done
