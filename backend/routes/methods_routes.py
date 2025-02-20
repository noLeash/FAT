import json
from fastapi import APIRouter, HTTPException, Query
from models.react_models import DropdownItem
from pathlib import Path
from pydantic import BaseModel
from typing import List
from typing import Dict, Any

methods_routes = APIRouter()


class MethodInput(BaseModel):
    method: str
    data: Dict[str, Any]

# Sample test data for menu
menu_data = [
    DropdownItem(id=1, title="Test Item 1", method="method_1"),
    DropdownItem(id=2, title="Test Item 2", method="method_2"),
]

# Sample markdown data
MOCK_MARKDOWN = {
    "example.md": "# Example Markdown\n\nThis is a test markdown file.",
    "info.md": "# Info Markdown\n\nSome informational content here."
}

# Endpoint to return test menu items
@methods_routes.get("/test/listof", response_model=List[DropdownItem])
async def get_test_menu_items():
    return menu_data

# Endpoint to return test markdown content
@methods_routes.get("/test/markdown/{filename}")
async def get_test_markdown(filename: str):
    content = MOCK_MARKDOWN.get(filename)
    if not content:
        raise HTTPException(status_code=404, detail="Markdown file not found")
    return content



# Mock schema data
SCHEMA_DATA = {
    "geometric_mean": {
        "title": "Geometric Mean",
        "description": "Calculate the geometric mean of a dataset.",
        "method": "geometric_mean",
        "fields": [
            {"name": "numbers", "type": "array", "format": "float", "label": "Numbers"},
        ],
        "markdown": "geometric_mean.md"
    },
    "arithmetic_mean": {
        "title": "Arithmetic Mean",
        "description": "Calculate the arithmetic mean of a dataset.",
        "method": "geo_mean",
        "fields": [
            {"name": "numbers", "type": "array", "format": "float", "label": "Numbers"},
        ],
        "markdown": "arithmetic_mean.md"
    },
    "coefficient_of_variance": {
        "title": "Coefficient of Variance",
        "description": "Calculate the coefficient of variance.",
        "method": "geo_mean",
        "fields": [
            {"name": "numbers", "type": "array", "format": "float", "label": "Numbers"},
        ],
        "markdown": "coefficient_variance.md"
    },
    "leveraged_returns": {
        "title": "Leveraged Return",
        "description": "Calculate the return on levered capital.",
        "method": "leveraged_returns",
        "fields": [
            {"name": "purchase_price", "type": "flaot", "format": "float", "label": "Purchase Price"},
            {"name": "borrowed", "type": "flaot", "format": "float", "label": "Amount Borrowed"},
            {"name": "debt_rate", "type": "percent", "format": "percent", "label": "Debt Rate"},
            {"name": "future_value", "type": "float", "format": "float", "label": "Future Value"}
        ],
        "markdown": "coefficient_variance.md"
    }
}

@methods_routes.get("/schema")
async def get_schema(method: str = Query(..., description="The method to fetch schema for")):
    """
    Fetches the schema based on the selected method.
    """
    # print(f"Method: {method}")
    schema = SCHEMA_DATA.get(method)
    # print(f"Schema: {schema}")
    if not schema:
        raise HTTPException(status_code=404, detail="Schema not found")

    return schema





# Base Processor Class
class MethodProcessor:
    """Base class for method processing"""
    
    def process(self, data: Dict[str, Any]) -> Any:
        """Override this in child classes"""
        raise NotImplementedError("Subclasses must implement this method")

# Processing Classes for Each Method
class GeometricMeanProcessor(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        numbers = data.get("numbers", [])
        if not numbers:
            raise ValueError("Numbers list is required")
        product = 1
        for num in numbers:
            product *= num
        return product ** (1 / len(numbers))

class ArithmeticMeanProcessor(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        numbers = data.get("numbers", [])
        if not numbers:
            raise ValueError("Numbers list is required")
        return sum(numbers) / len(numbers)

class CoefficientOfVarianceProcessor(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        numbers = data.get("numbers", [])
        if not numbers or len(numbers) < 2:
            raise ValueError("At least two numbers are required")
        mean = sum(numbers) / len(numbers)
        variance = sum((x - mean) ** 2 for x in numbers) / (len(numbers) - 1)
        return (variance ** 0.5) / mean if mean else None


class LeveragedReturn(MethodProcessor):
    def process(self, data: Dict[str, Any]) -> float:
        print(f"lev_retruns received: {data}")
        
        return "Nice Juan"

# Mapping of Methods to Their Processor Classes
METHOD_PROCESSORS: Dict[str, MethodProcessor] = {
    "geometric_mean": GeometricMeanProcessor(),
    "arithmetic_mean": ArithmeticMeanProcessor(),
    "coefficient_of_variance": CoefficientOfVarianceProcessor(),
    "leveraged_returns": LeveragedReturn()
}

# Input Schema
class MethodInput(BaseModel):
    method: str
    data: Dict[str, Any]

@methods_routes.post("/process")
async def process_method(input_data: MethodInput):
    """
    Dynamically selects the processing class based on the method.
    """

    print(f"INPUTDATA: {input_data}")
    method = input_data.method
    data = input_data.data

    # Validate method
    if method not in METHOD_PROCESSORS:
        raise HTTPException(status_code=400, detail=f"Method '{method}' not supported")

    processor = METHOD_PROCESSORS[method]

    try:
        result = processor.process(data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return {
        "method": method,
        "result": result,
        "message": f"Successfully processed {method}"
    }

