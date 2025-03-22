import json
import os
from fastapi import APIRouter, HTTPException, Query, FastAPI
from fastapi.responses import JSONResponse
from routes.functions_routes import load_schema
from models.methods import ibBars
from pathlib import Path
from pydantic import BaseModel
from typing import List
from typing import Dict, Any
import numpy as np
import math
# from methods import method_functions as mf
from methods.method_functions import METHOD_PROCESSORS

methods_routes = APIRouter()


class MethodInput(BaseModel):
    method: str
    data: Dict[str, Any]

app = FastAPI()


### Load Markdown
# Define the markdown file directory
MARKDOWN_DIR = "markdown_files"

# Markdown Route
@methods_routes.get("/markdown/{filename}")
async def get_markdown(filename: str):
    print(f"MARKDOWN CALLED")
    file_path = os.path.join(MARKDOWN_DIR, filename)
    print(file_path)
    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "Markdown file not found"})

    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return {"content": content}


### Load Schema
@methods_routes.get("/schema")
async def get_schema(method: str = Query(..., description="The method to fetch schema for")):
    """
    Fetches the schema based on the selected method.
    """
    print(f"Method: {method}")
    print(f'Schema {load_schema()}')
    schema = load_schema().get(method)
    # print(f"Schema: {schema}")
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")

    return schema


### Process Function
@methods_routes.post("/process")
async def process_method(input_data: MethodInput):
    """
    Dynamically selects the processing class based on the method.
    """

    # print(f"INPUTDATA: {input_data}")
    method = input_data.method
    data = input_data.data

    # Validate method
    print(METHOD_PROCESSORS)
    if method not in METHOD_PROCESSORS:
        raise HTTPException(status_code=400, detail=f"Method '{method}' not supported")

    processor = METHOD_PROCESSORS[method]

    try:
        # print(f"Data in: {data}")
        result = await processor.process(data)
        # print(f"Data out: {result}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "method": method,
        "result": result,
        "input": input_data,
        "message": f"Successfully processed {method}"
    }



