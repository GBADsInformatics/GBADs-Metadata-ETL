import load_data_helpers as dh
import pandas as pd
from database import get_db_driver
import sys
import argparse
import json

parser = argparse.ArgumentParser(
    description='Load data, metadata, categories, or other files into the graph database'
)

parser.add_argument('-p', '--filepath')
parser.add_argument('-f', '--format')
parser.add_argument('-t', '--type')
parser.add_argument('-n','--tablename')

args = parser.parse_args()
driver = get_db_driver()

if args.format == 'csv':
    df = pd.read_csv(args.filepath)
if args.format == 'json':
    with open(args.filepath, 'r') as file:
        df = json.load(file)

if args.type == 'Dataset':
    dh.load_dataset(df, driver)
if args.type == 'Organization':
    dh.load_organization(df. driver)
if args.type == 'PropertyValue':
    for index, row in df.iterrows():
        PropertyValue = row['PropertyValue']
        sourceTable = row['sourceTable']
        dh.connect_PropertyValue_Dataset(sourceTable, PropertyValue, driver)
if args.type == 'Value':
    for index, row in df.iterrows():
        Value = row['Value']
        sourceTable = args.tablename
        PropertyValue = row['parent']
        dh.connect_PropertyValue_Value(Value, sourceTable, PropertyValue, driver)

# df = pd.read_csv(cat_data_path)

# dh.load_cat_area(df, driver)