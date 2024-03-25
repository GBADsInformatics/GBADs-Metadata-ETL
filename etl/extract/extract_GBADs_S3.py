from extract_helpers import s3Helpers as s3h

resource = s3h.create_resource('aws-config.txt')

s3h.get_all_objects(resource, 'gbads-tables', '../../data/processed/s3-gbads-tables.json')