import pandas as pd
import json
from datetime import datetime
import csv
import sys
from validations import validate_metadata as vm
from pydantic import ValidationError
from validators import url

FAO_QCL_S3 = "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"
FAO_GLE_S3 = "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"
FAO_GLE_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_unfccc?fields=year,population,country,species,flag&query=&format=text"
FAO_QCL_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_faostat?fields=year,population,iso3,country,species,flag&query=&format=text"
FAO_GLE_TBL = "livestock_countries_population_unfccc"
FAO_QCL_TBL = "livestock_countries_population_faostat"

def load_from_json(json_file_path):
    # This should probably go in another module as a general-use function
    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset

def struct_DataDownload(db_dump, domain_code):

    datasets = db_dump.get('Datasets', {}).get('Dataset', [])

    for dataset in datasets: 
        if dataset['DatasetCode'] == domain_code:
            DataDownload = {
                'name': dataset['DatasetName'],
                'contentUrl': dataset['FileLocation'],
                'size': dataset['FileSize'],
                'encodingFormat': dataset['FileType']
            }
            return(DataDownload)

def struct_metadata(metadata, domain_code):

    metadata_fields = metadata.get('data', {})

    metadata_filtered = {}

    for i in metadata_fields:
        if 'metadata_text' in i:
            key = i['metadata_label']
            value = i['metadata_text']
            metadata_filtered[key] = value

    out_metadata = {
        'spatialCoverage': metadata_filtered.get('Reference area', ''),
        'description': metadata_filtered.get('Data description', ''),
        'license': metadata_filtered.get('User access',''),
        'temporalCoverage': metadata_filtered.get('Time coverage',''),
        'domainCode': domain_code
    }

    organization = {
        'url': metadata_filtered.get('Data Source',''),
        'name': metadata_filtered.get('Contact organization',''),
        'email': metadata_filtered.get('Contact email address','')
    }

    return(out_metadata, organization)

df = load_from_json('../../data/raw/faostat/20240226_dump.json')
DataDownload_QCL = struct_DataDownload(df, 'QCL')
DataDownload_GLE = struct_DataDownload(df, 'GLE')

try:
    # Create instances of models
    dataset = vm.DataDownload(**DataDownload_GLE)
    print(dataset)
except ValidationError as e:
    print(e)


# df = load_from_json('../../data/raw/faostat/20240226_GLE_metadata.json')
# metadata_GLE = struct_metadata(df, 'GLE')
# print(metadata_GLE)
# print(distribution_GLE)