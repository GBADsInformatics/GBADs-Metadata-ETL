from neo4j import GraphDatabase
from neo4j_backup import Extractor
import sys
sys.path.append("../load")
from database import get_db_driver

# Code adapted from: https://pypi.org/project/neo4j-backup/

if __name__ == "__main__":

    driver = get_db_driver()

    database = "neo4j"

    project_dir = "data_dump"
    input_yes = False
    compress = True
    indent_size = 4  # Indent of json files
    json_file_size: int = int("0xFFFF", 16)  # Size of data in memory before dumping
    extractor = Extractor(project_dir=project_dir, driver=driver, database=database,
                          input_yes=input_yes, compress=compress, indent_size=indent_size,
                          pull_uniqueness_constraints=True)
    extractor.extract_data()
