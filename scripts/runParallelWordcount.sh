#!/bin/bash

CORES=16
INPUT_DIR=/home/muntean/food-filter-tweets
OUTPUT_DIR=/home/muntean/food-outputs
COMMAND="time python ../wordcount/computeWordCount.py"

for LINE in `ls $INPUT_DIR/*.output`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/${OUTPUT_NAME}.output
done
sem --wait
exit 0
