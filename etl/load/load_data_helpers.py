import configparser
import os
from neo4j import GraphDatabase

# Read in config info from ini file 
## This function is from the GBADs-METADATA-API code 
def read_db_config(filename='config.ini', section='database'):
    
    if os.path.exists(filename): 
        parser = configparser.ConfigParser()
        parser.read(filename)
    else:
        try:
            filename='./load/config.ini'
            parser = configparser.ConfigParser()
            parser.read(filename)
        except: 
            raise Exception('Config file does not exist')
    
    db_config = {}
    if parser.has_section(section):
        items = parser.items(section)
        for item in items:
            db_config[item[0]] = item[1]
    else:
        raise Exception(f'{section} not found in the {filename} file')
    
    return db_config

def load_country(data, driver):
    # Load in country nodes 
    with driver.session() as session: 
        for d in data:
            print(d)
            query = (
                """
                MERGE (a:Country {name: $name})
                SET a.ISO2 = CASE WHEN $iso2 IS NOT NULL THEN $iso2 ELSE a.ISO2 END
                SET a.alternativeName = CASE WHEN $alternativeName IS NOT NULL THEN $alternativeName ELSE a.alternativeName END
                SET a.ISO3 = $iso3
                """
            )
            session.run(query, **d)

def update_dataset(data, driver):
    # Update dataset 
    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {sourceTable: $sourceTable})
            SET d.description = $description
            SET d.temporalCoverage = $temporalCoverage
            SET d.species = $species
            SET d.spatialCoverage = $spatialCoverage
            SET d.sourceTable = $sourceTable
            SET d.license = $license
            """
        )
        session.run(query, **data)

def load_dataset(data, driver):
    # Load in dataset nodes
    with driver.session() as session:
        query = (
            """
            MERGE (d:Dataset {name: $name})
            SET d.description = $description
            SET d.temporalCoverage = $temporalCoverage
            SET d.species = $species
            SET d.spatialCoverage = $spatialCoverage
            SET d.sourceTable = $sourceTable
            SET d.license = $license
            """
        )
        session.run(query, **data)

def load_organization(data, driver):
    # Load in organization node
    with driver.session() as session:
        query = (
            """
            MERGE (o:Organization {name: $name})
            SET o.url = $url
            SET o.email = $email
            """
        )
        session.run(query, **data)

def connect_organization(data, driver):
    # Load in organization node
    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {name: $dataset_name})
            WITH d
            MATCH (o:Organization {name: $name})
            WITH d,o
            MERGE (d)-[:HAS_CREATOR]->(o)
            """
        )
        session.run(query, **data)

def load_DataDownload(data, driver):

    with driver.session() as session:
        query = (
            """
            MERGE (d:DataDownload {contentUrl: $contentUrl})
            SET d.name = $name
            SET d.size = $size
            SET d.encodingFormat = $encodingFormat
            """
        )
        session.run(query, **data)

def connect_DataDownload(data, driver):

    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {name: $dataset_name})
            WITH d
            MERGE (d)-[:HAS_DISTRIBUTION]->(a:DataDownload {contentUrl: $contentUrl})
            """
        )
        session.run(query, **data)

def load_PropertyValue(data, driver):

    with driver.session() as session:
        query = (
            """
            MERGE (pv:PropertyValue {name: $name})
            SET pv.description = $description
            SET pv.unitText = $unitText
            """
        )
        session.run(query, **data)

def connect_PropertyValue_Dataset(data, driver):

    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {name: $datast_name})
            WITH d
            MERGE (d)-[:HAS_COLUMN]->(pv:PropertyValue {name: $name})
            """
        )
        session.run(query, **data)

def connect_PropertyValue_Value(data, driver):

    with driver.session() as session:
        query = (
            """
            MATCH (pv:PropertyValue {name: $name})
            WITH pv
            MERGE (pv)-[:HAS_VALUE]->(v:Value {name: $value})
            """
        )
        session.run(query, **data)

def connect_dataset_country(table_name, iso3, driver):

    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {sourceTable: $table_name})
            WITH d 
            MATCH (a:Value {ISO3: $iso3})
            MERGE (d)-[:HAS_COUNTRY]->(a)
            """
        )
        session.run(query, table_name = table_name, iso3 = iso3)