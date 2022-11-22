from typing import Any
from pydantic import BaseModel, Field


class DataverseInformation(BaseModel):
    base_url: str = Field(example="https://portal.odissei.nl/")
    dt_alias: str = Field(example="dans-easy")
    api_token: str = Field(example="12345678-ab12-12ab-abcd-a1b2c3d4e5g6")


class ImporterInput(BaseModel):
    metadata: list | dict | Any
    dataverse_information: DataverseInformation
