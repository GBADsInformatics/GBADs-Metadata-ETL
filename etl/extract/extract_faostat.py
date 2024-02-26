import pandas as pd
import json
import requests
import datetime

FAO_URL = 'https://fenixservices.fao.org/faostat/api/v1/'
FAO_CODES = ['QCL','GLE']
FAO_DUMP = 'https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'
FAO_RAW_DIR = '../../data/raw/faostat/'

def get_metadata(domain_code, lang='en', outdir = FAO_RAW_DIR):

    url = '{}/{}/metadata/{}'.format(FAO_URL,lang,domain_code)

    try:
        resp = requests.get(url)
    except requests.exceptions.RequestException as e:
        print('Error accessing API:', e)

    print(resp.json())
    

def get_db_dump(outdir = FAO_RAW_DIR):

    try:
        resp = requests.get(FAO_DUMP)
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)

    print(resp.json())

#def get_data_categories(domain_code, lang = 'en', outdir = FAO_RAW_DIR):

#def get_data(domain_code, lang = 'en', outdir = FAO_RAW_DIR):    

# print(get_db_dump())
# Download data from FAO API (dump) and from API. Save it in the raw data folder. 

