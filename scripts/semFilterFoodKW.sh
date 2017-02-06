#!/bin/bash

CORES=32
INPUT_DIR=/data/muntean/english-tweets
OUTPUT_DIR=/home/muntean/food-filter-tweets
COMMAND="time python ../filter/filterFoodKW.py"

for LINE in `ls $INPUT_DIR/*.gz`
do
	OUTPUT_NAME=`basename $LINE | cut -d'.' -f1`
	sem -j $CORES $COMMAND $LINE $OUTPUT_DIR/food-filter-${OUTPUT_NAME}.output
done
sem --wait
exit 0