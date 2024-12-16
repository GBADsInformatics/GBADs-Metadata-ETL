## This file is from the GBADs-METADATA-API code 

import os
from neo4j import GraphDatabase
from load_data_helpers import read_db_config

class Database:
    def __init__(self, test=False, dev=False):
        if os.environ.get('GRAPHDB_USERNAME') is None:
            if test:
                config = read_db_config(filename = 'config-test.ini')           
            elif dev:
                config = read_db_config(filename = 'config-dev.ini')
            else:
                config = read_db_config()
            self.driver = GraphDatabase.driver(config['uri'], auth=(config['username'], config['password']))
        else:
            self.driver = GraphDatabase.driver(os.environ.get('GRAPHDB_URI', None), auth=(os.environ.get('GRAPHDB_USERNAME', None), os.environ.get('GRAPHDB_PASSWORD', None)))

database = Database()
test_database = Database(test=True)
dev_database = Database(dev=True)

def get_db_driver(dev=False, test=False):
    if dev:
        return dev_database.driver
    if test:
        return test_database.driver
    return database.driver
