import load_data_helpers as dh
import pandas as pd
import json
from database import get_db_driver
import sys

driver = get_db_driver()

metadata_path = sys.argv[1]

with open(metadata_path, 'r') as file:
    metadata = json.load(file)

dh.load_dataset(metadata, driver)
