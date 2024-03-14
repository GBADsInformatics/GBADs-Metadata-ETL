#!/bin/sh

DATADIR=${1} #Specify data directory of interest
STRING=${2} #Specify the string of interest
NAME_OUT_FILE=${3} #Specify the name of the outfile

echo ""
echo ""
echo "Concatenating files in ${DATADIR} with string ${STRING}"
echo ""
echo ""

echo "Domain Code,Domain,Area Code,Area,Element Code,Element,Item Code,Item,Year Code,Year,Unit,Value,Flag,Flag Description,Note" > ${DATADIR}/${NAME_OUT_FILE}
for datafile in `ls ${DATADIR}`
do
  if [[ $datafile =~ $STRING ]] #If the name of the datafile contains the string
  then
    echo "Datafile with ${STRING} found!"
    echo "Processing ${datafile}"
    tail +2 ${DATADIR}/${datafile} >> ${DATADIR}/${NAME_OUT_FILE} #Cat contents of file except the header to current position in outfile
  fi
done