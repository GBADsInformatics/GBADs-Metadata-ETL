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