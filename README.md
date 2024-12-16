# 🐄 Global Burden of Animal Diseases (GBADs) Metadata Graph Database ETL (Extract, Transform, Load)

## Overview 

This repository contains the code and resources for extracting, transforming, and loading (ETL) data into the a Neo4j graph database. 

The graph database stores and manages metadata from data sources that are used for GBADs calculations and estimates. 

## Table of Contents 

- ✨[Introduction](#introduction)
- 🚀[Usage](#usage)
    - 👩‍💻[Using Database Dumps Locally](#database-local)
    - 🧙‍♂️[Interacting with the Graph Database in RStudio](#interacting-with-graph-database-in-rstudio)
- 🔄[ETL Process](#etl-process)
    - [Directory Structure](#directory-structure)
    - 📊[Data Sources](#data-sources)
- 📈[Graph Database Schema](#graph-database-schema)
- 🔎[Example Queries](#example-queries)
- 🤝[Contributing Data](#contributing)
    - 🌐[Contributing Data](#contributing-data)
- 🪪[License](#license)
- 🙏[Acknowledgements](#acknowledgements)

## ✨ Introduction

The Global Burden of Animal Diseases (GBADs) is a global research programme that uses livestock data from disperate sources to calculate national and global estimates of the economic and health burden of animal diseases.

To manage the Open data sources that GBADs uses, metadata and data from these sources is extracted, cleaned, and loaded into a graph database. This graph database serves as a repository of data, improving the discoverability of data used by GBADs. 

Beyond GBADs, this repository of livestock data can be used for researchers to discover data that may be useful in their work - we expect that this will be useful for climate change researchers, data scientists, epidemiologists and economists. 

💛🦄 *To suggest new sources of data for indexing, please check out the [Contributing Data](#contributing) section of this document* 

## 🚀 Usage

GBADs is currently using a paid Neo4j Aura instance to host the graph database. However, you are still able to interact with the graph database locally using database dumps.

### 👩‍💻 Using Database Dumps Locally

1. If you don't already have it, [download Neo4j Desktop](https://neo4j.com/download/?utm_source=google&utm_medium=PaidSearch&utm_campaign=GDB&utm_content=AMS-X-SEM-Category-Expansion-Evergreen-Search&utm_term=&gad_source=1&gclid=Cj0KCQiAoeGuBhCBARIsAGfKY7yA_XIMqEkjpnmwFmdLJR68V3VG9MZNZKGd1UYkQfBLlY3NQSYFswMaAg8wEALw_wcB)
2. Download the most recent dump file from the `data/dumps` directory
3. Follow the [restore a database dump](https://neo4j.com/docs/operations-manual/current/backup-restore/restore-dump/) instructions from Neo4j Docs 

### 🧙‍♂️ Interacting with Graph Database in RStudio 

Examples are provided in examples/query.Rmd

### Directory Structure

Some data files are omitted for the interest of space... 

```
.
├── LICENSE
├── README.md
├── config
├── data
│   ├── dumps
│   ├── processed
│   │   ├── ethiopia
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Camels_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Camels_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Camels_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Camels_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Cattle_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Cattle_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Cattle_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Cattle_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Donkeys_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Donkeys_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Donkeys_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Donkeys_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Goats_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Goats_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Goats_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Goats_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Horses_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Horses_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Horses_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Horses_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Mules_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Mules_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Mules_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Mules_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Poultry_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Poultry_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Poultry_table_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Poultry_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Sheep_cat_area_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Sheep_cat_yr.csv
│   │   │   ├── Ethiopia Central Statistics Agency Agricultural Sample Survey_Sheep_table_yr.csv
│   │   │   └── Ethiopia Central Statistics Agency Agricultural Sample Survey_Sheep_yr.csv
│   │   ├── eurostat
│   │   │   ├── 20240328_livestock_countries_population_eurostat_Dataset.json
│   │   │   ├── 20240328_livestock_countries_population_eurostat_area.csv
│   │   │   └── 20240328_livestock_countries_population_eurostat_category.csv
│   │   ├── faostat
│   │   │   ├── 20240328_livestock_countries_population_faostat_DataDownload.json
│   │   │   ├── 20240328_livestock_countries_population_faostat_Dataset.json
│   │   │   ├── 20240328_livestock_countries_population_faostat_Organization.json
│   │   │   ├── 20240328_livestock_countries_population_unfccc_DataDownload.json
│   │   │   ├── 20240328_livestock_countries_population_unfccc_Dataset.json
│   │   │   └── 20240328_livestock_countries_population_unfccc_Organization.json
│   │   ├── geo
│   │   ├── s3-gbads-tables.json
│   │   └── woah
│   │       ├── 20240403_livestock_countries_population_oie_DataDownload.json
│   │       ├── 20240403_livestock_countries_population_oie_Dataset.json
│   │       ├── 20240403_livestock_countries_population_oie_Organization.json
│   │       ├── 20240403_livestock_countries_population_oie_PropertyValue.csv
│   │       ├── 20240403_livestock_countries_population_oie_area.csv
│   │       └── 20240403_livestock_countries_population_oie_category.csv
│   └── raw
│       ├── ethiopia
│       │   ├── 2003_102.csv
│       │   ├── 2003_103.csv
│       │   ├── 2003_104.csv
│       │   ├── 2003_105.csv
│       │   ├── 2003_106.csv
│       │   ├── 2004_132.csv
│       │   ├── 2004_133.csv
│       │   ├── 2020_186.csv
│       │   ├── 2020_187.csv
│       │   ├── 2020_188.csv
│       │   ├── 2020_189.csv
│       │   ├── 2020_190.csv
│       │   ├── EthCSA_Camels.csv
│       │   ├── EthCSA_Cattle.csv
│       │   ├── EthCSA_Donkeys.csv
│       │   ├── EthCSA_Goats.csv
│       │   ├── EthCSA_Horses.csv
│       │   ├── EthCSA_Mules.csv
│       │   ├── EthCSA_Poultry.csv
│       │   ├── EthCSA_Sheep.csv
│       │   └── EthCSA_allCats.csv
│       ├── eurostat
│       │   └── 20240328_livestock_countries_population_eurostat.csv
│       ├── faostat
│       │   ├── 20240226_GLE_itemcodes.json
│       │   ├── 20240226_GLE_metadata.json
│       │   ├── 20240226_QCL_itemcodes.json
│       │   ├── 20240226_QCL_metadata.json
│       │   ├── 20240226_dump.json
│       │   ├── 20240325_GLE_description.txt
│       │   ├── 20240325_QCL_description.txt
│       │   ├── S3
│       │   │   ├── livestock_countries_population_faostat.csv
│       │   │   └── livestock_countries_population_unfccc.csv
│       │   ├── Y0226_areacodes.json
│       │   └── data
│       │       ├── 20240313_en_GLE_100_filtered.csv
│       │       ├── 20240313_en_GLE_101_filtered.csv
│       │       ├── 20240313_en_GLE_102_filtered.csv
│       │       ├── 20240313_en_GLE_103_filtered.csv
│       │       ├── 20240313_en_GLE_104_filtered.csv
│       ├── geo
│       │   └── 20240309_geo.csv
│       ├── indonesia
│       │   ├── 20230824_Indonesia_BeefCattle.xlsx
│       │   ├── 20230824_Indonesia_Broiler.xlsx
│       │   ├── 20230824_Indonesia_Buffalo.xlsx
│       │   └── 20230824_Indonesia_DairyCattle.xlsx
│       ├── ireland
│       │   ├── dataset.json
│       │   ├── datasets.csv
│       │   ├── meta_AAA01.json
│       │   ├── meta_AAA02.json
│       │   ├── meta_AAA03.json
│       │   ├── meta_AAA04.json
│       │   ├── meta_AAA05.json
│       │   ├── meta_AAA06.json
│       │   ├── meta_AAA07.json
│       │   ├── meta_AAA08.json
│       │   ├── meta_AAA09.json
│       │   ├── meta_AAA10.json
│       │   ├── meta_AAA11.json
│       │   ├── meta_ACEN1.json
│       │   ├── meta_AVA11.json
│       │   ├── meta_AVA12.json
│       │   └── meta_FSA14.json
│       └── woah
│           ├── 20240320_WOAH_Metadata.json
│           ├── 20240320_WOAH_Organization.json
│           └── 20240326_livestock_countries_population_oie.csv
├── docs
│   ├── Countries.md
│   ├── ETHIOPIA.md
│   ├── EuroStat.md
│   ├── FAOSTAT.md
│   ├── Indonesia.md
│   ├── Ireland.md
│   └── WOAH.md
├── etl
│   ├── combine_datasets.sh
│   ├── etl_country.py
│   ├── extract
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── extract_faostat.cpython-312.pyc
│   │   │   └── extract_helpers.cpython-312.pyc
│   │   ├── aws-config.txt
│   │   ├── extract_GBADs_S3.py
│   │   ├── extract_ess.py
│   │   ├── extract_eurostat.py
│   │   ├── extract_faostat.py
│   │   ├── extract_helpers.py
│   │   ├── extract_indonesia.py
│   │   ├── extract_ireland.R
│   │   └── extract_woah.py
│   ├── load
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-312.pyc
│   │   │   ├── database.cpython-312.pyc
│   │   │   ├── load.cpython-312.pyc
│   │   │   ├── load_data.cpython-312.pyc
│   │   │   └── load_data_helpers.cpython-312.pyc
│   │   ├── config-test.ini
│   │   ├── config.ini
│   │   ├── database.py
│   │   ├── load_data.py
│   │   ├── load_data_helpers.py
│   │   ├── load_woah.sh
│   │   └── update_dataset.py
│   └── transform
│       ├── __init__.py
│       ├── __pycache__
│       │   ├── transform_helpers.cpython-312.pyc
│       │   └── validate_metadata.cpython-312.pyc
│       ├── transform_ethiopia.py
│       ├── transform_faostat.py
│       ├── transform_from_file.py
│       ├── transform_helpers.py
│       ├── transform_ireland.R
│       └── validate_metadata.py
├── examples
│   └── query.Rmd
├── graph-db-schema.png
├── tests
│   ├── __pycache__
│   │   ├── test_graph_database.cpython-312-pytest-7.4.4.pyc
│   │   └── test_graph_database.cpython-312.pyc
│   ├── test_data
│   │   ├── test_datadownload.json
│   │   ├── test_dataset.json
│   │   └── test_organization.json
│   └── test_graph_database.py
└── tmp.txt

32 directories, 948 files


```

### 📊 Data Sources

Data sources use different standards to report, disseminate, structure and format their data and metadata. Therefore, each data source usually needs an independent set of tools to extract and transform it into the database. Once it is transformed into a common format, it can be loaded in the graph database.

Therefore, each data source has a unique directory in the `data/` directory.

## 📈 Graph Database Schema 

<img src='graph-db-schema.png' alt='Graph Database Schema' width="300"/>

FIXME add more info about actual schema validation

### Nodes

DataDownload: https://schema.org/DataDownload


## 🔎 Example Queries

This repository is linked to the [GBADs-Metadata-API](https://github.com/GBADsInformatics/GBADs-Metadata-API) repository, which provides queries, tools, and tests to query the graph database.

<!-- ## ⚡️ Performance Optimization

The performance optimization strategy: https://neo4j.com/docs/operations-manual/current/performance/

### Batch Size 

### Indexing 

### Cypher Query Optimization -->

## 🤝 Contributing

We would love to see others contribute code. Since we are using a fully-managed Neo4j Aura service, contributions to code are restricted to metadata extraction and preparation. 

### 🌐 Contributing Data

If you have a new data source that you'd like to contribute or see added to the metadata store, we would love your input. 
* To contribute data, create an issue in this repository. 
* Please provide a *direct* link to your dataset (not just a landing page). 
* If a direct link is not available, please provide *instructions* on how to access the data of interest. 
* Please provide a link to the licensing information or use instructions for the dataset. We are only adding *Open* data to the graph.

If the data of interest is in a PDF table, please also share. We will mark it with an additional tag and consider scraping it. 

<!-- ## 🪪 License  -->


<!-- ## Disclaimer

This project is provided "as-is" with no warranties or guarantees. Use it at your own risk. The maintainers and contributors are not responsible for any damages or liabilities related to the use, modification, or distribution of this project. -->

## 🙏 Acknowledgments

We acknowledge the support of the Bill and Melinda Gates Foundation. 

This work has been conducted, in part, for my PhD work which is funded by the Natural Sciences and Engineering Research Council of Canada (NSERC) CGS-D award. 

