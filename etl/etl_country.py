import pandas as pd
import json
import sys 
from datetime import datetime
from extract import extract_helpers as eh
from load import load
from transform.validations import validate_metadata as vm

data_dir = '../data/'

# Get country data from API 
data = eh.GBADsAPI.make_call(eh.GEO_TBLS)
headers = data[:1]
df = pd.DataFrame(data[1:])
df.columns = headers
df.columns = df.columns.map('_'.join)

# Save a time stamped version in the raw data dir 
today = datetime.today().strftime('%Y%m%d')
raw_file = "{}raw/geo/{}_geo.csv".format(data_dir, today)
df.to_csv(raw_file, index=False)

# Read and Transform
# Read in data 
dff = pd.read_csv(raw_file, encoding='latin1')

# Rename columns
cols = ['name', 'alternativeName', 'iso3', 'iso2', 'uni', 'undp', 'faostat', 'gaul']
dff.columns = cols
dff = dff[['name', 'alternativeName', 'iso3', 'iso2']]

df_json = dff.to_json(orient='records')
df_dict = json.loads(df_json)

# Validate
errors = 0
for country in df_dict:
    try:
        Country = vm.Country(**country)
    except Exception as e:
        print(f"Validation error for {country}: {e}")
        errors += 1

if errors > 1:
    sys.exit(-1)

# Load
