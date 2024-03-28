import pandas as pd
import json
import requests
from datetime import datetime
import sys
import csv
from extract_helpers import GBADsAPI

out_path = '../../data/raw/eurostat'

url = 'https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_eurostat?fields=year,population,country,species,flag&query=&format=text' 

data = GBADsAPI.make_call(url)

df = pd.DataFrame(data)

columns = df.iloc[0]

df = df.drop(df.index[0])

df.columns = columns

date = datetime.today().strftime('%Y%m%d')

outfile = '%s/%s_livestock_countries_population_eurostat.csv' % (out_path, date)
df.to_csv(outfile, index=False)