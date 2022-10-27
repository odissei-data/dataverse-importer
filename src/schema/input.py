from typing import Any
from pydantic import BaseModel


class DataverseInformation(BaseModel):
    base_url: str
    dt_alias: str
    api_token: str


class ImporterInput(BaseModel):
    metadata: list | dict | Any
    dataverse_information: DataverseInformation
