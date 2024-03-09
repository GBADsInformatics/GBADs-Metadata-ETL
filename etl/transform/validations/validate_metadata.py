from pydantic import BaseModel, Field, validator, ValidationError
import datetime
from validators import url
import sys
import requests

def validate_url(value:str) -> str:
    # First check in valid url
    if url(value) == 'False':
        raise ValueError("Validation Failed: Invalid URL")
        sys.exit(-1)
    # Now check url response status
    try:
        response = requests.head(value)
        response.raise_for_status()
    except requests.RequestException as e:
        raise ValueError("Validation Failed: Could not download data from URL")
        sys.exit(-1)
    return(value)

class Dataset(BaseModel):
    name: str
    description: str
    spatialCoverage: str
    temporalCoverage: str
    sourceTable: str | None
    license: str
    species: str | None

    @validator("license", pre=True)
    def validate_url(cls, value: str | None) -> str:
        if not url(value):
            return("Unknown")
        return(value)

class Organization(BaseModel):
    name: str
    address: str | None
    url: str

    @validator("url", pre=True)
    def validate_org_url(cls, value:str) -> str:
        return(validate_url(value))

class DataDownload(BaseModel):
    # Should we also be testing against a controlled vocab? 
    contentUrl: str
    name: str
    size: str
    encodingFormat: str

    @validator("contentUrl", pre=True)
    def validate_content_url(cls, value:str) -> str:
        return(validate_url(value))

    # @validator("size", pre=True)
    # def validate_size(cls, value:str) -> str:
    #     value_num = size[:-2]
    #     try:
    #         size_in_kb = int(value)
    #         if size_in_kb <= 0:
    #             raise ValueError("Size must be greater than 0")
    #     except ValueError:
    #         raise ValueError("Invalid size format or non-positive size")
    #     return(value)

class Person(BaseModel):
    name: str
    address: str | None
    department: str | None
    jobTitle: str | None
    email: str | None

