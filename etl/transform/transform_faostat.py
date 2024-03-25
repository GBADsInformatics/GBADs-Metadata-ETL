import pandas as pd
import json
from datetime import datetime
import csv
import sys
# from transform.validations import validate_metadata as vm
from pydantic import ValidationError
from validators import url
import transform_helpers as th

FAO_QCL_S3 = "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"
FAO_GLE_S3 = "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"
FAO_GLE_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_unfccc?fields=year,population,country,species,flag&query=&format=text"
FAO_QCL_GBADS_API = "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_faostat?fields=year,population,iso3,country,species,flag&query=&format=text"
FAO_GLE_TBL = "livestock_countries_population_unfccc"
FAO_QCL_TBL = "livestock_countries_population_faostat"

def get_cat(df):
    """
    Extracts unique categories from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing a column named 'Item'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column.
    """

    cats = df['Item'].unique()

    df_cats = pd.DataFrame(cats, columns = ['category'])

    return(df_cats)

def get_cat_yr(df):
    """
    Extracts unique categories and the years that they occur in from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing columns named 'Item' and 'Year'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column and the years that they occur in.
    """
    
    df_cat_yrs = df.groupby(['Item'])['Year'].unique().apply(list).reset_index()

    df_cat_yrs.columns = ['category','year']
    
    return(df_cat_yrs)

def get_cat_yr_area(df):
    """
    Extracts unique categories and the years and countries that they occur in from the 'Item' column of the input DataFrame.

    Parameters:
    df (pd DataFrame): Input DataFrame containing columns named 'Item', 'Year', and 'Area'.

    Returns:
    pd DataFrame: DataFrame containing unique categories extracted from the 'Item' column and the years and countries that they occur in.
    """

    df_cat_yr_area = df.groupby(['Item','Area'])['Year'].unique().apply(list).reset_index()
    
    df_cat_yr_area.columns = ['category','area','year']

    return(df_cat_yr_area)


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

if __name__ == "__main__":

    path = sys.argv[1]

    df = pd.read_csv(path)

    # For each of the following create output files 

    cats = get_cat(df)
    print(cats)
    
    # With each of the categories present in the dataset, we want the definition of each and the related codes.

    cat_yrs = get_cat_yr(df)

    print(cat_yrs)
    cat_yr_area = get_cat_yr_area(df)

    print(cat_yr_area)


# df = load_from_json('../../data/raw/faostat/20240226_dump.json')
# DataDownload_QCL = struct_DataDownload(df, 'QCL')
# DataDownload_GLE = struct_DataDownload(df, 'GLE')

# try:
#     # Create instances of models
#     dataset = vm.DataDownload(**DataDownload_GLE)
#     print(dataset)
# except ValidationError as e:
#     print(e)


# df = load_from_json('../../data/raw/faostat/20240226_GLE_metadata.json')
# metadata_GLE = struct_metadata(df, 'GLE')
# print(metadata_GLE)
# print(distribution_GLE)