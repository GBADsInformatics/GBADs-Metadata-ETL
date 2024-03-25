import requests
import pandas as pd
import json
import csv
import boto3
import sys
import datetime
import math

GEO_TBLS = "https://gbadske.org/api/GBADsPublicQuery/un_geo_codes?fields=*&query=&format=text"

def convert_size(size_bytes):
    """
    This function is from: https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
    """
    if size_bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def load_from_json(json_file_path):
    # This should probably go in another module as a general-use function
    with open(json_file_path, 'r') as file:
        dataset = json.load(file)

    return dataset

class s3Helpers:

    @staticmethod
    def create_resource(path_auth): 

        """ 
        Takes path to authentification info (txt file) and creates boto3 resource 
        """

        # Open auth access key 
        f = open(path_auth, "r")
        for line in f: 
            if 'aws_access_key_id' in line:
                mykey = line.rstrip('\n').split('=')[1]
            if 'aws_secret_access_key' in line: 
                mysecretkey = line.rstrip('\n').split('=')[1]

        s3 = boto3.resource(
            service_name='s3',
            region_name='ca-central-1',
            aws_access_key_id=mykey,
            aws_secret_access_key=mysecretkey
        )

        return(s3)

    @staticmethod    
    def get_all_buckets(s3):
        for bucket in s3.buckets.all():
            print(bucket.name) 

    @staticmethod
    def get_all_objects(s3, bucket_name, out_path):

        """
        For a given bucket, get all objects 
        Returns object size, key, and date that it was last modified 
        """

        bucket = s3.Bucket(bucket_name)

        data = {}

        for obj in bucket.objects.all():

            if obj.size > 0:

                name = obj.key
                date = obj.last_modified
                date = date.strftime('%Y-%m-%d')
                contentUrl = 'https://%s.%s/%s' % (bucket_name,'s3.ca-central-1.amazonaws.com', obj.key)
                size = obj.size 
                
                # Size is in bytes 
                size = convert_size(size)

                data[name] = {'size': size, 'contentUrl': contentUrl, 'lastModified': date}

        with open(out_path, 'w') as f:
            json.dump(data, f, indent=2)


class GBADsAPI: 

    @staticmethod
    def get_content_size(url):

        r = requests.get(url)
        content_size = len(r.content)
        
        return(content_size)

    @staticmethod
    def construct_api_call(table_name): 

        base_url = 'https://gbadske.org/api/GBADsPublicQuery/'
        query = '?fields=*&query=&format=html'
        url = '%s%s%s' % (base_url, table_name, query)

        return(url)

    @staticmethod
    def test_call(url): 

        r = requests.get(url)
        if r.status_code == 404:
            return(0)
        else: 
            return(1)

    @staticmethod
    def make_call(url): 

        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

        return(my_list)

    @staticmethod
    def get_eth_tbls():
            
        eth_tbl_url = 'http://gbadske.org/api/GBADsTables/public?format=text'
        
        tbls = GBADsAPI.make_call(eth_tbl_url)
        
        tbls = pd.Series(tbls[0])

        # Get a list of all tables that start with Eth region
        eth_tbls = tbls[tbls.str.contains('eth_region')]

        return(eth_tbls)