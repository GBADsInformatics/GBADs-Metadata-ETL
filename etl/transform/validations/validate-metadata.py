from pydantic import BaseModel, Field, validator, Coordinate, ValidationError
import datetime
from validators import url

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
    def validate_url(cls, value:str) -> str:
        if not url(value):
            return("Unknown")
        return(value)

class DataDownload(BaseModel):
    contentUrl: str
    name: str
    encodingFormat: str

    @validator("contentUrl", pre=True)
    def validate_url(cls, value:str) -> str:
        if not url(value):
            return("Unknown")
        return(value)

class Person(BaseModel):
    name: str
    address: str | None
    department: str | None
    jobTitle: str | None
    email: str | None

