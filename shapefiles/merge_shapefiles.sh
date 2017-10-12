#!/bin/bash -x

# Service that appends ESRI Shapefiles from an input directory into given output file

if [ "$#" -ne 3 ]
then
    echo 'Usage: append_files.sh input_dir output_dir filename(no extension)'
else
    
    INPUT_DIR=$1
    OUTPUT_DIR=$2
    OUTFILE=$3

    # Function that makes sure that directories have / at the end
    function check_directory {
	local dir1=$1
	x="${dir1: -1}"
	if [ "$x" != '/' ];
	then
	    dir1=${dir1}/
	fi
	echo $dir1
    }
    
    INPUT_DIR=$(check_directory "$INPUT_DIR")
    OUTPUT_DIR=$(check_directory "$OUTPUT_DIR")

    # Create output directory if it does not exist
    if [ ! -e "$OUTPUT_DIR" ]
    then
	mkdir -p $OUTPUT_DIR
    fi

    # Delete output file if it exists
    filename=${OUTPUT_DIR}${OUTFILE}.shp
    if [ -e "$filename" ]
    then
	echo 'Removing output file'
	rm $filename
    fi

    # Copy first input file (and its companion files - shx, xml, prj) into the output directory, otherwise, append the layers from other shp files
    for infile in ${INPUT_DIR}*.shp
    do
	echo $infile
	if [ ! -e "$filename" ]
    	then
	    echo 'First input file, create a copy.'
    	    ogr2ogr -f "ESRI Shapefile" $filename $infile
    	else
	    echo 'Append.'
	    ogr2ogr -update -append -f "ESRI Shapefile" $filename $infile 
    	fi
    done  
    
fi
