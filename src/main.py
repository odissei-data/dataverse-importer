import json
import os
import requests
from urllib.parse import urlparse

from fastapi import FastAPI, HTTPException
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
    version="0.1.2",
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
    # Validate base_url against whitelist to prevent SSRF
    allowed_urls_env = os.getenv("ALLOWED_BASE_URLS", "")
    if not allowed_urls_env:
        raise HTTPException(status_code=500, detail="ALLOWED_BASE_URLS not configured")
    allowed_urls = [url.strip() for url in allowed_urls_env.split(",") if url.strip()]

    base_url = importer_input.dataverse_information.base_url
    parsed = urlparse(base_url)
    normalized_base_url = f"{parsed.scheme}://{parsed.netloc}"

    if normalized_base_url not in allowed_urls:
        raise HTTPException(
            status_code=400,
            detail=f"base_url not allowed."
        )

    headers = {
        "X-Dataverse-key": importer_input.dataverse_information.api_token,
        "Content-type": "application/json"
    }
    create_url = f"{base_url}" \
                 f"/api/dataverses/" \
                 f"{importer_input.dataverse_information.dt_alias}" \
                 f"/datasets/:import?pid={importer_input.doi}&release=no"

    response = requests.post(create_url, headers=headers,
                             json=importer_input.metadata)

    if not response.ok:
        raise HTTPException(status_code=response.status_code,
                            detail=response.text)
    return response.json()
