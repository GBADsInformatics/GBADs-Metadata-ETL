## This file is from the GBADs-METADATA-API code 

import os
from neo4j import GraphDatabase
from load.load_data import read_db_config as read_db_config

class Database:
    def __init__(self):
        if os.environ.get('GRAPHDB_USERNAME') is None:
            config = read_db_config()
            self.driver = GraphDatabase.driver(config['uri'], auth=(config['username'], config['password']))
        else:
            self.driver = GraphDatabase.driver(os.environ.get('GRAPHDB_URI', None), auth=(os.environ.get('GRAPHDB_USERNAME', None), os.environ.get('GRAPHDB_PASSWORD', None)))

database = Database()

def get_db_driver():
    return database.driver