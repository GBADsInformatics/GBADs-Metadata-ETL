import pandas as pd
import json
from datetime import datetime
import csv
import sys
# from transform.validations import validate_metadata as vm
from pydantic import ValidationError
from validators import url
import transform_helpers as th
import requests

FAO_GLE_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_unfccc?fields=year,population,country,species,flag&query=&format=text"
FAO_QCL_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_faostat?fields=year,population,iso3,country,species,flag&query=&format=text"
FAO_GLE_TBL = "livestock_countries_population_unfccc"
FAO_QCL_TBL = "livestock_countries_population_faostat"
FAO_DESCRIPTION = ""
FAO_LISENCE = "https://creativecommons.org/licenses/by-nc-sa/3.0/igo"
FAO_METADATA_BASE_URL = "https://www.fao.org/faostat/en/#data/"

def filter_db_dump(db_dump, domain_code):
    """
    For a domain code, extracts and maps the fields of interest. Note that the description is not taken from this file because as of 2024-03-20, the description was just the name of the organization

    Parameters:
    db_dump (json): Input file containing the database dump from FAOSTAT. 

    Returns:
    Dataset (dict): a dictionary containing the dataset name, description, and dateModified 
    """

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

def get_organization(metadata):

    metadata_fields = metadata.get('data', {})

    metadata_filtered = {}

    for i in metadata_fields:
        if 'metadata_text' in i:
            key = i['metadata_label']
            value = i['metadata_text']
            metadata_filtered[key] = value
    
        organization = {
        'url': metadata_filtered.get('Data Source',''),
        'name': metadata_filtered.get('Contact organization',''),
        'email': metadata_filtered.get('Contact email address','')
        }
    return(organization)

def create_custom_metadata(dataset_name, domain_code):

    if domain_code == 'QCL':
        sourceTable = FAO_QCL_TBL
    else:
        sourceTable = FAO_GLE_TBL

    metadata = {
        'name': dataset_name,
        'description': FAO_DESCRIPTION,
        'license': FAO_LISENCE,
        'sourceTable': sourceTable
    }

    return(metadata)


# def create_metadata(metadata, domain_code):

#     metadata_fields = metadata.get('data', {})

#     metadata_filtered = {}

#     for i in metadata_fields:
#         if 'metadata_text' in i:
#             key = i['metadata_label']
#             value = i['metadata_text']
#             metadata_filtered[key] = value

#     out_metadata = {
#         'spatialCoverage': metadata_filtered.get('Reference area', ''),
#         'description': metadata_filtered.get('Data description', ''),
#         'license': metadata_filtered.get('User access',''),
#         'temporalCoverage': metadata_filtered.get('Time coverage','')
#     }

#     return(out_metadata)

# def prep_save_metadata(db_dump_file_path, metadata_file_path, domain_code):

#     db_dump_file = th.load_from_json(db_dump_file_path)
#     metadata_file = th.load_from_json(metadata_file_path)

#     DataDownload = filter_db_dump(db_dump_file, domain_code)

#     Dataset = 

#     Categories = 

#     Coverage = 

#     Organization = get_organization(metadata_file)

#     return(Dataset, DataDownload, Organization, Categories, Coverage)

