import configparser
import os
from neo4j import GraphDatabase

# Read in config info from ini file 
## This function is from the GBADs-METADATA-API code 
def read_db_config(filename='config.ini', section='database'):

    parser = configparser.ConfigParser()

    possible_paths = [
        filename,
        os.path.join(os.path.dirname(__file__), filename),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../load', filename))
    ]
    
    config_found = False
    for path in possible_paths:
        if os.path.exists(path): 
            parser.read(path)
            config_found = True
            break
    
    if not config_found: 
        raise Exception(f'Config file not found in specified locations.')

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

def load_dataset(data, driver, return_query = False):
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

        if return_query == True:
            return_query = (
                """
                MATCH (d:Dataset {name: $name})
                RETURN d.name AS name, d.description AS description
                """
            )
            result = session.run(return_query, name = data['name'])    
            record = result.single()

            return(record)
    
def load_organization(data, driver, return_query = False):
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
    
        if return_query == True:
            return_query = (
                """
                MATCH (o:Organization {name: $name})
                RETURN o.name AS name, o.url AS url, o.email AS email
                """
            )
            result = session.run(return_query, name = data['name'])
            record = result.single()

            return(record)

def connect_organization(org_name, dataset_name, driver):
    # Load in organization node
    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {sourceTable: $dataset_name})
            WITH d
            MATCH (o:Organization {name: $name})
            WITH d,o
            MERGE (d)-[:HAS_CREATOR]->(o)
            """
        )
        session.run(query, name=org_name, dataset_name=dataset_name)

def load_DataDownload(data, driver, return_query = False):

    with driver.session() as session:
        query = (
            """
            MATCH (a:Dataset {sourceTable: $name})
            MERGE (a)-[:HAS_DISTRIBUTION]->(d:DataDownload {contentUrl: $contentUrl})
            SET d.name = $name
            SET d.size = $size
            SET d.encodingFormat = $encodingFormat
            """
        )
        session.run(query, **data)
    
        if return_query == True:
            return_query = (
                """
                MATCH (a:Dataset)-[r:HAS_DISTRIBUTION]->(d:DataDownload {contentUrl: $contentUrl})
                WHERE a.name = $name
                RETURN a.name AS name, d.contentUrl AS contentUrl
                """
            )
            result = session.run(return_query, name = data['name'], contentUrl = data['contentUrl'])
            record = result.single()

            return(record)

def connect_PropertyValue_Dataset(dataset_name, name, driver):

    with driver.session() as session:
        query = (
            """
            MATCH (d:Dataset {sourceTable: $dataset_name})
            WITH d
            MERGE (d)-[:HAS_COLUMN]->(pv:PropertyValue {name: $name})
            """
        )
        session.run(query, dataset_name=dataset_name, name=name)

def connect_PropertyValue_Value(value, sourceTable, PropertyValue, driver):
    try:
        with driver.session() as session:
            query = """
            MATCH (d:Dataset {sourceTable: $sourceTable})-[:HAS_COLUMN]->(pv:PropertyValue {name: $PropertyValue})
            MERGE (v:Value {name: $value})
            MERGE (pv)-[:HAS_VALUE]->(v)
            """
            result = session.run(query, sourceTable=sourceTable, PropertyValue=PropertyValue, value=value)
            return(result)

    except Exception as e:
        print("An error occurred:", str(e))
        return None


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
