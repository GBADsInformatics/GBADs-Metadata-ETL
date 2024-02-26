import pandas as pd
import json
import requests
from datetime import datetime

FAO_URL     = 'https://fenixservices.fao.org/faostat/api/v1/'
FAO_CODES   = ['QCL','GLE']
FAO_DUMP    = 'https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'
FAO_RAW_DIR = '../../data/raw/faostat/'

def get_metadata(domain_code, lang='en', outdir = FAO_RAW_DIR):

    url = '{}/{}/metadata/{}'.format(FAO_URL,lang,domain_code)
    time = datetime.today().strftime('%Y%m%d')
    outfile_path = '{}{}_{}_metadata.json'.format(FAO_RAW_DIR, time, domain_code)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e:
        print('Error accessing API:', e)

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)
    

def get_db_dump(outdir = FAO_RAW_DIR):

    time = datetime.today().strftime('%y%m%d')
    outfile_path = '{}{}_dump.json'.format{FAO_RAW_DIR, time}

    try:
        resp = requests.get(FAO_DUMP)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)

#def get_data_categories(domain_code, lang = 'en', outdir = FAO_RAW_DIR):

#def get_data(domain_code, lang = 'en', outdir = FAO_RAW_DIR):    

# get_metadata('QCL')