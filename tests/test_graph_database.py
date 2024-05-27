from neo4j import GraphDatabase
import pytest
import sys
import os
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../etl/load')))
from load_data_helpers import read_db_config
import load_data_helpers as ldh
import database

def load_test_data(filename):
    with open(filename, 'r') as file:
        return(json.load(file))

def test_read_db_config():
    # Test to see if read config can read the config file s

    try:
        config = read_db_config('test_config.ini', 'database')
        assert config['host'] == 'localhost'
        print('Test with default config passed.')
    except Exception as e:
        print(f'Test with default config failed: {e}')
    
    # Test with a config file in the fallback directory
    try:
        config = read_db_config('non_existent_config.ini', 'database')
        print('Test with fallback directory config passed.')
    except Exception as e:
        print(f'Test with fallback directory config failed: {e}')
    
    # Test with missing section
    try:
        config = read_db_config('test_config.ini', 'non_existent_section')
        print('Test with missing section passed.')
    except Exception as e:
        print(f'Test with missing section failed: {e}')


def test_load_dataset():
    # Load test data from file
    data = load_test_data('tests/test_data/test_dataset.json')
    driver = database.get_db_driver(test=True)
    result = ldh.load_dataset(data, driver, return_query = True)

    assert result["name"] == data["name"]
    assert result["description"] == data["description"]

    
# def test_load_organization():
#     data = load_test_data('tests/test_data/test_organization.json')
#     driver = database.get_db_driver(test=True)


# def test_insert_organization(graph_db):
#     organization = graph_db.create_node("Organization", name="OpenAI", industry="AI Research")
#     assert organization is not None
#     assert organization["name"] == "OpenAI"
#     assert organization["industry"] == "AI Research"

# def test_insert_dataset(graph_db):
#     dataset = graph_db.create_node("Dataset", name="Sample Dataset", size=1000)
#     assert dataset is not None
#     assert dataset["name"] == "Sample Dataset"
#     assert dataset["size"] == 1000

# def test_insert_datadownload(graph_db):
#     datadownload = graph_db.create_node("DataDownload", url="http://example.com/data", format="CSV")
#     assert datadownload is not None
#     assert datadownload["url"] == "http://example.com/data"
#     assert datadownload["format"] == "CSV"

# def test_insert_propertyvalue(graph_db):
#     property_value = graph_db.create_node("PropertyValue", property="Height", value="180cm")
#     assert property_value is not None
#     assert property_value["property"] == "Height"
#     assert property_value["value"] == "180cm"

# def test_insert_value(graph_db):
#     value = graph_db.create_node("Value", value="Some Value")
#     assert value is not None
#     assert value["value"] == "Some Value"

if __name__ == "__main__":
    pytest.main()
