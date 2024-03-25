import json

def load_from_json(json_file_path):

    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset