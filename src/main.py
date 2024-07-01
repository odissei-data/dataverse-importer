import json

from fastapi import FastAPI, HTTPException
from pyDataverse.api import NativeApi

from schema.input import ImporterInput
from version import get_version

description = """
This dataverse-importer API can be used to import metadata into a given
 dataverse.

"""

tags_metadata = [
    {
        "name": "version",
        "description": "Returns the version of this API",
    },
    {
        "name": "importer",
        "description": "Imports metadata into a given Dataverse",
        "externalDocs": {
            "description": "This API uses the Dataverse Native API",
            "url": "https://guides.dataverse.org/en/latest/api/",
        },
    },
]

app = FastAPI(
    title="dataverse-importer",
    description=description,
    version="0.1.1",
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata
)


@app.get("/version", tags=["version"])
async def info():
    result = get_version()
    return {"version": result}


@app.post("/importer", tags=["importer"])
def import_metadata(importer_input: ImporterInput):
    metadata = json.dumps(importer_input.metadata)
    api = NativeApi(importer_input.dataverse_information.base_url,
                    importer_input.dataverse_information.api_token)

    response = api.create_dataset(
        importer_input.dataverse_information.dt_alias,
        metadata, pid=importer_input.doi)

    if not response.ok:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)
    return response.json()
