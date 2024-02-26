import pandas as pd
import json
from datetime import datetime
import csv
import sys

def load_from_json(json_file_path):

    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset

def struct_dump(db_dump, domain_code):

    datasets = db_dump.get('Datasets', {}).get('Dataset', [])

    for dataset in datasets: 
        if dataset['DatasetCode'] == domain_code:
            distribution = {
                'name': dataset['DatasetName'],
                'domainCode': dataset['DatasetCode'],
                'contentUrl': dataset['FileLocation'],
                'size': dataset['FileSize'],
                'encodingFormat': dataset['FileType']
            }
            return(distribution)

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

#df = load_from_json('../../data/raw/faostat/20240226_dump.json')
#distribution = struct_dump(df, 'QCL')

#df = load_from_json('../../data/raw/faostat/20240226_GLE_metadata.json')
#struct_metadata(df, 'GLE')