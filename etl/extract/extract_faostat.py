import pandas as pd
import json
import requests

FAO_CODES = ['QCL','GLE']
FAO_API = 'https://fenixservices.fao.org/faostat/api/v1/en/metadata/'
FAO_DUMP = 'https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json'


