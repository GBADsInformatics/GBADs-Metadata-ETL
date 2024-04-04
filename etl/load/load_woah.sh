#!/bin/sh

DATADIR=${1} #Specify data directory of interest
TABLENAME=${2}
DATE=${3}

echo ""
echo ""
echo "Loading data from ${TABLENAME}"
echo ""
echo ""

# DatasetNode=${DATADIR}/${DATE}_${TABLENAME}_Dataset.json
# echo "Loading Dataset Node from ${DatasetNode}"
# python3 load_data.py -p ${DatasetNode} -f json -t Dataset -n ${TABLENAME}

OrganizationNode=${DATADIR}/${DATE}_${TABLENAME}_Organization.json
echo "Loading and connecting Organization Node from ${OrganizationNode}"
python3 load_data.py -p ${OrganizationNode} -f json -t Organization -n ${TABLENAME}



# echo "Loading and connecting PropertyValues"

# python3 load_cat_data.py -p ../../data/processed/woah/20240403_livestock_countries_population_oie_category.csv -f csv -t Value -n livestock_countries_population_oie

# for datafile in `ls ${DATADIR}`
# do
#   if [[ $datafile =~ $STRING ]] #If the name of the datafile contains the string
#   then
#     echo "Datafile with ${STRING} found!"
#     echo "Processing ${datafile}"
#     tail +2 ${DATADIR}/${datafile} >> ${DATADIR}/${NAME_OUT_FILE} #Cat contents of file except the header to current position in outfile
#   fi
# done