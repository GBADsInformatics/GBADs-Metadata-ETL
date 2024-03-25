# Food and Agriculture Organization of the United Nations Statistical Database 

## Datasets 

There are 3 sources of livestock population data from FAOSTAT: 

Domain: Production/Crops and livestock products
Elements: Stocks
URL: https://www.fao.org/faostat/en/#data/QCL
* This data source is available at: "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"

Domain: Climate Change: Agrifood system emissions/Emissions from Livestock
Elements: Stocks
FAO SOURCE: FAO TIER 1
URL: https://www.fao.org/faostat/en/#data/GLE
* This data source is available at: "https://gbads-tables.s3.ca-central-1.amazonaws.com/International/livestock_countries_population_faostat.csv"
* "https://gbadske.org/api/GBADsPublicQuery/livestock_countries_population_unfccc?fields=year,population,country,species,flag&query=&format=text"

Domain: Climate Change: Agrifood system emissions/Emissions from Livestock
Elements: Stocks
FAO SOURCE: UNFCCC
URL: https://www.fao.org/faostat/en/#data/GLE

Each of the datasets from these sources was downloaded and 

## Creating Metadata 

### Metadata from Source 

There a few ways you can get metadata from FAOSTAT: 

1. Through direct download on the user interface
2. Database description (available in json and XML)
    * https://fenixservices.fao.org/faostat/static/bulkdownloads/datasets_E.json
    * This provides a dump of metadata for all datasets in FAOSTAT. Note that the metadata provided here is not same as the metadata provided by direct download on the user interface.
3. Fenix Services API 
    * https://fenixservices.fao.org/faostat/api/v1/
    * https://fenixservices.fao.org/faostat/api/v1/en/groupsanddomains/
    * https://fenixservices.fao.org/faostat/api/v1/en/dimensions/QCL/
    * Bulk downloads: https://fenixservices.fao.org/faostat/api/v1/en/bulkdownloads/QCL 
    * Metadata: https://fenixservices.fao.org/faostat/api/v1/en/metadata/QCL/
    * Flags: https://fenixservices.fao.org/faostat/api/v1/en/definitions/types/flag

The database description is useful because it provides a minimum set of metadata and the file size, number of rows, and file location. Therefore this can be used to create the distribution nodes. On the other hand, the description is not very descriptive and the topic provides an address, not actual topics. 
    
For example: 

```
{"DatasetCode":"QCL","DatasetName":"Production: Crops and livestock products","Topic":"Viale delle Terme di Caracalla, 00153 Rome, Italy","DatasetDescription":"Food and Agriculture Organization of the United Nations (FAO)","Contact":null,"Email":null,"DateUpdate":"2023-12-18T00:00:00","CompressionFormat":"zip","FileType":"csv","FileSize":"32546KB","FileRows":4127584,"FileLocation":"https://fenixservices.fao.org/faostat/static/bulkdownloads/Production_Crops_Livestock_E_All_Data_(Normalized).zip"}
```

The fenix services Metadata link provides complete metadata information in json format. There is much more metadata provided than we would like to make available in the graph database, therefore we can link to the metadata if the user/viewer would like more information about the dataset. 

### Information from datasets 

In addition to the metadata, we need a list of species that are provided in the data, the countries that they are provided for, and the years that data are available for. 

To get the data, I ran `extract_faostat.py` in the `etl/extract directory`. 
I then combined all the datasets using the `combine_datasets.sh` program

## Other useful links: 

https://www.fao.org/statistics/caliper/tools/download/en