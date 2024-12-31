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
import validate_metadata as vm

FAO_GLE_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_unfccc?fields=year,population,country,species,flag&query=&format=text"
FAO_QCL_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_faostat?fields=year,population,iso3,country,species,flag&query=&format=text"
FAO_GLE_TBL = "livestock_countries_population_unfccc"
FAO_QCL_TBL = "livestock_countries_population_faostat"
FAO_LICENSE = "https://creativecommons.org/licenses/by-nc-sa/3.0/igo"
FAO_METADATA_BASE_URL = "https://www.fao.org/faostat/en/#data/"

def get_dataset_name(db_dump, domain_code):

    datasets = db_dump.get('Datasets', {}).get('Dataset', [])

    for dataset in datasets:
        if dataset['DatasetCode'] == domain_code:
            name = dataset['DatasetName']

    return(name)

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

def create_custom_metadata(dataset_name, domain_code, file_path, description):

    if domain_code == 'QCL':
        sourceTable = FAO_QCL_TBL
    else:
        sourceTable = FAO_GLE_TBL

    df = pd.read_csv(file_path)

    species = th.get_cat(df, 'species')
    spatialCoverage = th.get_cat(df, 'country')
    temporalCoverage = th.get_temporal_coverage(df, 'year')

    metadata = {
        'name': dataset_name,
        'description': description,
        'license': FAO_LICENSE,
        'sourceTable': sourceTable,
        'species': species,
        'temporalCoverage': temporalCoverage,
        'spatialCoverage': ['World']
    }

    return(metadata)

if __name__ == "__main__":

    # For each of the datasets from FAOSTAT we need to create the following, and then we need to put them together: 
    # The 'base metadata' 
    # The DataDownload nodes (S3, data dump from FAOSTAT)
    # The "included in data catalogue" - information about the data catalogue
    # Organization information, which is also creator 
    # Property Values (names of columns, and also units, description where applicable) 
    # Values (embedded in the PropertyValue) - if the value is a country, we don't need both the ISO3 code and the country name, we just need the ISO3 code 

    out_path = sys.argv[1]
    domain_code = sys.argv[2]

    db_dump_file = '../../data/raw/faostat/20240226_dump.json'
    src_metadata_file = '../../data/raw/faostat/20240226_%s_metadata.json' % domain_code
    file_path = '../../data/raw/faostat/S3/livestock_countries_population_faostat.csv'
    description_path = '../../data/raw/faostat/20240325_%s_description.txt' % domain_code

    db_dump = th.load_from_json(db_dump_file)
    src_metadata = th.load_from_json(src_metadata_file)
    df = pd.read_csv(file_path)
    description = th.get_descriptions_txt(description_path)

    name = get_dataset_name(db_dump, domain_code)
    data_download = filter_db_dump(db_dump, domain_code)
    dataset = create_custom_metadata(name, domain_code, file_path, description)
    src_tbl = dataset['sourceTable']
    organization = get_organization(src_metadata)
    property_values = th.get_cols(df)

    # Validate metadata
    try:
        DataDownload = vm.DataDownload(**data_download)
    except ValidationError as e:
        sys.exit(e)
    th.write_metadata(out_path, data_download, src_tbl, 'DataDownload')


    # Validate dataset 
    try:
        Dataset = vm.Dataset(**dataset)
    except ValidationError as e: 
        sys.exit(e)
    th.write_metadata(out_path, dataset, src_tbl, 'Dataset')

    th.write_metadata(out_path, organization, src_tbl, 'Organization')
    