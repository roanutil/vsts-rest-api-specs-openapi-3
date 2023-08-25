from pathlib import Path
from urllib import request
from http.client import HTTPResponse
import os

# Naively find all spec files and update them to openapi 3.0.x and convert to yaml
for specFolder in Path(__file__).parent.resolve().joinpath(Path("specification")).glob("*"):
    for specVersionFolder in specFolder.glob("*"):
        for spec in specVersionFolder.glob("*.json"):
            newSpec = spec.with_suffix(".yaml")
            print(spec)
            print(newSpec)
            httpRequestBody = open(spec, "rb")
            headers = {
                "accept": "application/yaml", 
                "Content-Type": "application/json",
                "Content-Length": os.stat(spec).st_size,
            }
            httpRequest = request.Request(url="https://converter.swagger.io/api/convert", data=httpRequestBody, headers=headers, method="POST")
            response: HTTPResponse = request.urlopen(httpRequest)
            responseData = response.read()
            newSpec.write_bytes(responseData)
