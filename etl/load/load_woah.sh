#!/bin/sh

DATADIR=${1} #Specify data directory of interest
TABLENAME=${2}
DATE=${3}

echo ""
echo ""
echo "Loading data from ${TABLENAME}"
echo ""
echo ""

DatasetNode=${DATADIR}/${DATE}_${TABLENAME}_Dataset.json
echo "Loading Dataset Node from ${DatasetNode}"
python3 load_data.py -p ${DatasetNode} -f json -t Dataset -n ${TABLENAME}

OrganizationNode=${DATADIR}/${DATE}_${TABLENAME}_Organization.json
echo "Loading and connecting Organization Node from ${OrganizationNode}"
python3 load_data.py -p ${OrganizationNode} -f json -t Organization -n ${TABLENAME}

PropertyValue=${DATADIR}/${DATE}_${TABLENAME}_PropertyValue.csv
echo "Loading and connecting PropertyValues from ${PropertyValue}"
python3 load_data.py -p ${PropertyValue} -f csv -t PropertyValue -n ${TABLENAME}

SpeciesValue=${DATADIR}/${DATE}_${TABLENAME}_category.csv 
echo "Loading and connecting Values to PropertyValues from ${SpeciesValue}"
python3 load_data.py -p ${SpeciesValue} -f csv -t Value -n ${TABLENAME}

CountryValue=${DATADIR}/${DATE}_${TABLENAME}_area.csv
echo "Loading and connecting Values to PropertyValues from ${CountryValue}"
python3 load_data.py -p ${CountryValue} -f csv -t Value -n ${TABLENAME}

