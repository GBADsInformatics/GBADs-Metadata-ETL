import pandas as pd
import json
from datetime import datetime
import sys
from pydantic import ValidationError
from validators import url
import transform_helpers as th
import validate_metadata as vm

file_path = sys.argv[1]
metadata_path = sys.argv[2]
out_path = sys.argv[3]

# Get woah species, temporal cov and spatial coverage 
df = pd.read_csv(file_path)

temporalCoverage = th.get_temporal_coverage(df, 'year')
spatialCoverage = th.get_cat(df, 'country')
species = th.get_cat(df, 'species')

# Read in metadata file and add in spatial coverage, temporal coverage, species 
metadata = th.load_from_json(metadata_path)
metadata['species'] = species
metadata['spatialCoverage'] = spatialCoverage
metadata['temporalCoverage'] = temporalCoverage

# Validate metadata
try:
    Dataset = vm.Dataset(**metadata)
except ValidationError as e:
    sys.exit(e)

th.write_metadata(out_path, metadata, metadata['sourceTable'], 'Dataset')

# Create country, parent df
area_parent = th.get_cat_yr(df, 'country', 'year', columns = ['Value','year'])
area_parent['parent'] = 'country'
th.write_parent_child(out_path, area_parent, metadata['sourceTable'], 'area')

# Create category, parent df
category_parent = th.get_cat_yr(df, 'species', 'year', columns = ['Value','year'])
category_parent['parent'] = 'species'
th.write_parent_child(out_path, category_parent, metadata['sourceTable'], 'category')

# Create source, propertyVale
source = metadata['sourceTable']
columns = th.get_cols(df)
src_propvalue = pd.DataFrame(columns)
src_propvalue['sourceTable'] = source
src_propvalue.columns = ['PropertyValue','sourceTable']
th.write_parent_child(out_path, src_propvalue, source, 'PropertyValue') 