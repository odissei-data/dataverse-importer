import json
import requests

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from schema.input import ImporterInput, FileInput
from pydantic import ValidationError
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
        "description": "Imports metadata and data into a given Dataverse",
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
    headers = {
        "X-Dataverse-key": importer_input.dataverse_information.api_token,
        "Content-type": "application/json"
    }
    create_url = f"{importer_input.dataverse_information.base_url}" \
                 f"/api/dataverses/" \
                 f"{importer_input.dataverse_information.dt_alias}" \
                 f"/datasets/:import?pid={importer_input.doi}&release=no"
    if not importer_input.doi:
        create_url = f"{importer_input.dataverse_information.base_url}" \
                    f"/api/dataverses/" \
                    f"{importer_input.dataverse_information.dt_alias}" \
                    f"/datasets"

    response = requests.post(create_url, headers=headers,
                             json=importer_input.metadata)

    if not response.ok:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)
    return response.json()

@app.post('/file-upload', tags=['importer'])
async def add_file(json_data: str = Form(...), file: UploadFile = File(...)):
    try:
        print(json_data)
        jsonstring = json.loads(json_data)
        # Parse and validate json_data with the Pydantic model
        parsed_data = FileInput(**jsonstring)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors())

    headers = {
        "X-Dataverse-key": parsed_data.dataverse_information.api_token,
    }
    dataverse_url = parsed_data.dataverse_information.base_url
    file_url = f"{dataverse_url}" \
                 f"/api/datasets/:persistentId/add"
    params = {
        'persistentId': parsed_data.doi,
        'key': parsed_data.dataverse_information.api_token
    }
    filecontent = await file.read()
    files = {'file': (
        file.filename, filecontent
    )}
    response = requests.post(
        url=file_url,
        headers=headers,
        files=files,
        params=params
    )
    if not response.ok:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)
    return response.json()
