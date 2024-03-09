# Country Names

## Datasets

To ensure that we can search by countries, and to connect the countries to the datasets, we have to load in country names.

We also want ISO codes and M49 codes when possible.

The `un_geo_codes` data table provides ISO codes and country names.

This API call downloads the data: https://gbadske.org/api/GBADsPublicQuery/un_geo_codes?fields=*&query=&format=text

We may also explore the use of geonames for adding more data, particulary alternative country names and subnational administrative regions. 

## Metadata:
*  https://schema.org/Country


## Ingestion pipeline
The data is extracted, transformed, validated and loaded using the `etl/etl_country.py` scipt.
