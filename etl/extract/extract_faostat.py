import pandas as pd
import json
import requests
from datetime import datetime
import sys
import csv

FAO_URL     = 'https://fenixservices.fao.org/faostat/api/v1/'
FAO_CODES   = ['QCL','GLE']
FAO_DUMP    = 'https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'
FAO_RAW_DIR = 'data/raw/faostat/'

def filter_element_qcl(df, elements = ['Stocks', 'Milk Animals','Laying']):
    """
    Filter the FAOSTAT QCL dataset to filter dataset by elements.

    Parameters:
        df (pandas DataFrame): A pandas df of data from the QCL dataset from FAOSTAT.
        elements (list, optional): A list of elements to filter by. Default is ['Stocks','Milk Animals'].

    Returns:
        dff (pandas DataFrame): A DataFrame filtered based on the elements given.
    """
    try:
        
        dff = df.loc[df['Element'].isin(elements)] 
        return(dff)
    
    except KeyError as e:

        print('Error filtering dataset %s' % e)


def get_metadata(domain_code, lang='en', outdir = FAO_RAW_DIR):

    """
    Get metadata for a specified domain code and save it as a JSON file.

    Parameters:
        domain_code (str): The code representing the domain code from FAOSTAT.
        lang (str, optional): Language code for the metadata (default is 'en'). Not entirely sure which languages are actually supported.
        outdir (str, optional): The directory path to save the file (default is FAO_RAW_DIR).

    Returns:
        None
    """

    url = '{}/{}/metadata/{}'.format(FAO_URL,lang,domain_code)
    time = datetime.today().strftime('%Y%m%d')
    outfile_path = '{}{}_{}_metadata.json'.format(outdir, time, domain_code)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print('Error accessing API:', e)
        sys.exit()

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)
    
    print('Metadata from url: {} downloaded and saved in {}'.format(url, outfile_path))
    

def get_db_dump(outdir = FAO_RAW_DIR):

    """
    Get database description from FAOSTAT and save it as a JSON file.

    Parameters:
        outdir (str, optional): The directory path to save the file (default is FAO_RAW_DIR).

    Returns:
        None
    """

    time = datetime.today().strftime('%Y%m%d')
    outfile_path = '{}{}_dump.json'.format(outdir, time)

    try:
        resp = requests.get(FAO_DUMP)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)
        sys.exit()

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)
    
    print('FAOSTAT database dump successfully downloaded from: {}'.format(FAO_DUMP))

def get_areagroup(outdir = FAO_RAW_DIR, lang = 'en'):
    """
    Get area group codes used by FAOSTAT and save them as a json file.

    Parameters:
        lang (str, optional): Language code for the metadata (default is 'en'). Not entirely sure which languages are actually supported.
        outdir (str, optional): The directory path to save the file (default is FAO_RAW_DIR).

    Returns:
        None
    """

    url = '{}/{}/definitions/types/areagroup'.format(FAO_URL,lang)
    
    time = datetime.today().strftime('Y%m%d')
    outfile_path = '{}{}_areacodes.json'.format(outdir, time)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)   

    print('Area groups downloaded from: {}'.format(url)) 

def get_itemcodes(domain_code, lang = 'en', outdir = FAO_RAW_DIR):
    """
    Get item codes for a specified domain code and save them in a JSON file.

    Parameters:
        domain_code (str): The code representing the domain code from FAOSTAT.
        lang (str, optional): Language code for the metadata (default is 'en'). Not entirely sure which languages are actually supported.
        outdir (str, optional): The directory path to save the file (default is FAO_RAW_DIR).

    Returns:
        None
    """

    url = '{}/{}/definitions/domain/{}/item'.format(FAO_URL, lang, domain_code)

    time = datetime.today().strftime('%Y%m%d')
    outfile_path = '{}{}_{}_itemcodes.json'.format(outdir, time, domain_code)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)
        sys.exit()

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)  
    
    print('Item codes for {} downloaded from {}'.format(domain_code, url))

def get_all_country_codes(lang = 'en'):

    """
    Get area country codes in the World (Country Group Code = 5000) used by FAOSTAT and return them as a list.

    Parameters:
        lang (str, optional): Language code for the metadata (default is 'en'). Not entirely sure which languages are actually supported.

    Returns:
        country_codes (list): A list of country codes contained in country group world (5000)
    """

    url = '{}/{}/definitions/types/areagroup'.format(FAO_URL,lang)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)

    df = pd.DataFrame(data['data'])
    dff = df.loc[df['Country Group Code'] == '5000']
    country_codes = dff['Country Code'].reset_index(drop=True)

    country_codes = country_codes.to_list()
    
    return(country_codes)

def get_data(domain_code, area_code, format = 'csv', lang = 'en', outdir = FAO_RAW_DIR):  
    """
    Get data for a specified domain and area code, and save it as a JSON or csv file.

    Parameters:
        domain_code (str): The code representing the domain code from FAOSTAT.
        area_code (str): The code representing the area of interest from FAOSTAT. Use the get_areagroup function to find all area codes.
        format (str, optional): Format of outfile (default is csv). Accepted values include json , csv or none.
        lang (str, optional): Language code for the metadata (default is 'en'). Not entirely sure which languages are actually supported.
        outdir (str, optional): The directory path to save the file (default is FAO_RAW_DIR).

    Returns:
        None
    """

    if format not in ['json','csv','None']:
        print('Invalid format: {}. Accepted formats for outfile include csv or json.')
        sys.exit()

    url = '{}/{}/data/{}?area={}'.format(FAO_URL, lang, domain_code, area_code)
    
    print(url)

    time = datetime.today().strftime('%Y%m%d')
    outfile_path = '{}{}_{}_{}_{}.{}'.format(outdir, time, lang, domain_code, area_code, format)

    try:
        resp = requests.get(url)
        data = resp.content
        # Data comes back in type bytes, so need to convert it to something sensible
        data = json.loads(data)
    except requests.exceptions.RequestException as e: 
        print('Error getting data:', e)
        sys.exit()
    
    df = pd.DataFrame(data['data'])

    if format == 'csv':

        # Change to pandas df

        df = pd.DataFrame(data['data'])
        
        df.to_csv(outfile_path, index = False)

    if format == 'json':

        with open(outfile_path, 'w') as json_file:
            json.dump(data, json_file) 
        
    if format == 'None':

        df = pd.DataFrame(data['data'])
        return(df)

    print('FAOSTAT data with domain code {} and area code {} downloaded in {}'.format(domain_code, area_code, outdir))

if __name__ == "__main__":

    fao_code = sys.argv[1]

    # Get data from FAOSTAT 
    country_codes = get_all_country_codes()

    for i in country_codes:

        df = get_data(fao_code,i, format = 'None')

        print('Data fetched for %s %s' % (fao_code, i))

        path = '../../data/raw/faostat/data/20240313_en_%s_%s.csv' % (fao_code, i)

        try:

            dff = filter_element_qcl(df)
            
            outfile = '../../data/raw/faostat/data/20240313_en_%s_%s_filtered.csv' % (fao_code, i)

            dff.to_csv(outfile, index = False)

            print('Dataset filtered: %s' % path)
        
        except Exception as e:
            print('Dataset %s could not be loaded due to %s' % (path, e))
