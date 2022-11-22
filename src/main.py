import json

from fastapi import FastAPI
from pyDataverse.api import NativeApi

from schema.input import ImporterInput
from version import get_version

app = FastAPI()


@app.get("/version")
async def info():
    result = get_version()
    return {"version": result}


@app.post("/importer")
def import_metadata(importer_input: ImporterInput):
    metadata = json.dumps(importer_input.metadata)
    api = NativeApi(importer_input.dataverse_information.base_url,
                    importer_input.dataverse_information.api_token)
    response = api.create_dataset(
        importer_input.dataverse_information.dt_alias,
        metadata)
    return response.json()
