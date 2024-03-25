from pydantic import BaseModel, Field, validator, ValidationError
from typing import Optional
import datetime
from validators import url
import sys
import requests

def validate_url(value:str) -> str:
    if not url(value):
        raise ValueError("Validation Failed: Invalid URL")
        sys.exit(-1)

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
    license: str | None
    species: str | None

    @validator("license", pre=True)
    def validate_url(cls, value: str | None) -> str:
        return(validate_url(value))

class Organization(BaseModel):
    name: str
    address: str | None
    url: str | None

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

class Person(BaseModel):
    name: str
    address: str | None
    department: str | None
    jobTitle: str | None
    email: str | None

class Country(BaseModel):
    name: str
    alternativeName: str | None
    iso2: str | None
    iso3: str
    M49: Optional[str] = None