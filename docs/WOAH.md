# World Organization for Animal Health (WOAH) Data 

The World Organization for Animal Health (WOAH) provided livestock population data to GBADs.

Currently, the data does not include metadata. Therefore, we had to create our own descriptive metadata.

## Creating Metadata 

* The temporal and spatial range, and species were extracted from the database table 
* The license was found online at: "https://wahis.oie.int/#/tnc"
* We created a name for the dataset based on its contents 
* We created our own description for the dataset based on its contents 

### Extract

`python3 extract_woah.py`

### Transform and (Validate)

`python3 transform_from_file.py ../../data/raw/woah/20240326_livestock_countries_population_oie.csv ../../data/raw/woah/20240320_WOAH_Metadata.json ../../data/processed/woah`

### Load 

To load the data, the script `load_woah.sh` can be used with the following: 

`./load_woah.sh ../../data/processed/woah livestock_countries_population_oie 20240403`