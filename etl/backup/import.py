from neo4j import GraphDatabase
from neo4j_backup import Importer
import sys
sys.path.append("../load")
from database import get_db_driver

# Code adapted from: https://pypi.org/project/neo4j-backup/

if __name__ == "__main__":

    driver = get_db_driver(dev=True)

    database = "neo4j"

    project_dir = "data_dump"
    input_yes = False
    importer = Importer(project_dir=project_dir, driver=driver, database=database, input_yes=input_yes)
    importer.import_data()