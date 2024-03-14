from extract import extract_faostat as ex_fao
from transform import transform_faostat as tr_fao
import pandas as pd
import json
import sys 

# Download metadata 

# for i in ex_fao.FAO_CODES:

#     ex_fao.get_metadata(i)
#     ex_fao.get_itemcodes(i)

# # Download database dump and area group codes

# ex_fao.get_areagroup()
# ex_fao.get_db_dump()

# Get data from FAOSTAT 
country_codes = ex_fao.get_all_country_codes()

#for i in country_codes:

    # ex_fao.get_data('QCL',i, outdir='../data/raw/faostat/data/')

for i in country_codes: 
    df = pd.read_csv('../data/raw/faostat/data/20240313_en_QCL_33.csv')

    dff = ex_fao.filter_element_qcl(df)
    print(dff)

# ex_fao.get_data('QCL',')