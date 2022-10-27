import json

from fastapi import FastAPI
from pyDataverse.api import NativeApi
from pyDataverse.models import Dataset
from pyDataverse.utils import read_file

from schema.input import ImporterInput
from version import get_version

app = FastAPI()


@app.get("/version")
async def info():
    result = get_version()
    return {"version": result}


@app.post("/importer")
def map_metadata(importer_input: ImporterInput):

    ds = Dataset()
    filename = "output.json"
    with open(filename, 'w') as outfile:
        json.dump(importer_input.metadata, outfile)
    ds.from_json(read_file(filename))
    api = NativeApi(importer_input.dataverse_information.base_url,
                    importer_input.dataverse_information.api_token)
    response = api.create_dataset(
        importer_input.dataverse_information.dt_alias,
        ds.json())
    return response.json()
