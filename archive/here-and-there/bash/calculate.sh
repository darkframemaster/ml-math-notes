#!/bin/bash

echo "5+50*3/20" | bc -l
echo "(19*2)/7" | bc -l
four=`echo "scale = 4; 5+50*3/20 + (19*2)/7" | bc -l`
three=`echo "scale = 3; 5+50*3/20 + (19*2)/7" | bc -l`
compare=`echo "$four-$three" | bc -l` 

if [ $( echo "$compare >= 0.0005" | bc ) -eq 1 ]
then
    echo "scale = 3; $three + 0.001" | bc -l
else
    echo $three
fi
