import pandas as pd
import json
import requests
from datetime import datetime
import sys
import csv
from extract_helpers import GBADsAPI

start_year = 2005
end_year = 2020
out_path = '../../data/raw/woah'

all_data = []

for year in range(start_year, end_year):  

    url = 'https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_oie?fields=year,population,country,species,flag&query=year=%s&format=text' % year

    data = GBADsAPI.make_call(url)

    df = pd.DataFrame(data)
    
    columns = df.iloc[0]
    
    df = df.drop(df.index[0])

    all_data.append(df)

all_data = pd.concat(all_data)
all_data.columns = columns

date = datetime.today().strftime('%Y%m%d')

outfile = '%s/%s_livestock_countries_population_oie.csv' % (out_path, date)
all_data.to_csv(outfile, index=False)
