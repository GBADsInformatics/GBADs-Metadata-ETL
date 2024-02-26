import pandas as pd
import json
import requests
from datetime import datetime
import sys
import csv

FAO_URL     = 'https://fenixservices.fao.org/faostat/api/v1/'
FAO_CODES   = ['QCL','GLE']
FAO_DUMP    = 'https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'
FAO_RAW_DIR = '../../data/raw/faostat/'

def get_metadata(domain_code, lang='en', outdir = FAO_RAW_DIR):

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
    

def get_db_dump(outdir = FAO_RAW_DIR):

    time = datetime.today().strftime('%y%m%d')
    outfile_path = '{}{}_dump.json'.format(outdir, time)

    try:
        resp = requests.get(FAO_DUMP)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)
        sys.exit()

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)

def get_areagroup(outdir = FAO_RAW_DIR, lang = 'en'):

    url = '{}/{}/definitions/types/areagroup'.format(FAO_URL,lang)
    
    time = datetime.today().strftime('%y%m%d')
    outfile_path = '{}{}_areacodes.json'.format(outdir, time)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)    

def get_itemcodes(domain_code, lang = 'en', outdir = FAO_RAW_DIR):

    url = '{}/{}/definitions/domain/{}/item'.format(FAO_URL, lang, domain_code)

    time = datetime.today().strftime('%y%m%d')
    outfile_path = '{}{}_{}_itemcodes.json'.format(outdir, time, domain_code)

    try:
        resp = requests.get(url)
        data = resp.json()
    except requests.exceptions.RequestException as e: 
        print('Error getting db dump:', e)
        sys.exit()

    with open(outfile_path, 'w') as json_file:
        json.dump(data, json_file)  
    

def get_data(domain_code, area_code, format = 'csv', lang = 'en', outdir = FAO_RAW_DIR):  

    if format not in ['json','csv']:
        print('Invalid format: {}. Accepted formats for outfile include csv or json.')
        sys.exit()

    url = '{}/{}/data/{}?area={}'.format(FAO_URL, lang, domain_code, area_code)
    
    time = datetime.today().strftime('%y%m%d')
    outfile_path = '{}{}_{}_{}.{}'.format(time, lang, domain_code, area_code, format)

    try:
        resp = requests.get(url)
        data = resp.content
    except requests.exceptions.RequestException as e: 
        print('Error getting data:', e)
        sys.exit()
    
    if format == 'csv':

        with open(outfile_path, 'wb') as csv_file:
            csv_file.write(data)

    if format == 'json':

        with open(outfile_path, 'w') as json_file:
            json.dump(data, json_file) 
        
    print('FAOSTAT data with domain code {} and area code {} downloaded in {}'.format(domain_code, area_code, outdir))