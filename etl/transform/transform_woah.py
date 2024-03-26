import pandas as pd
import json
from datetime import datetime
import sys
from pydantic import ValidationError
from validators import url
import transform_helpers as th
from validations import validate_metadata as vm

file_path = sys.argv[1]
metadata_path = sys.argv[2]
org_path = sys.argv[3]
out_path = sys.argv[4]

# Get woah species, temporal cov and spatial coverage 
df = pd.read_csv(file_path)

temporalCoverage = th.get_temporal_coverage(df, 'year')
spatialCoverage = th.get_cat(df, 'country')
species = th.get_species(df, 'species')

# Read in metadata file and add in spatial coverage, temporal coverage, species 
metadata = th.load_from_json(metadata_path)
metadata['species'] = species
metadata['spatialCoverage'] = spatialCoverage
metadata['temporalCoverage'] = temporalCoverage

