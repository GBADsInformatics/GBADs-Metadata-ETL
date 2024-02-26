from extract import extract_faostat as ex_fao
from transform import transform_faostat as tr_fao
import pandas as pd
import json
import sys 

# Download metadata 

for i in ex_fao.FAO_CODES:

    ex_fao.get_metadata(i)
    ex_fao.get_itemcodes(i)

# Download database dump and area group codes

ex_fao.get_areagroup()
ex_fao.get_db_dump()