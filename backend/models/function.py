from pydantic import BaseModel
from typing import List, Dict, Optional

class FunctionField(BaseModel):
    name: str
    label: str
    type: str
    placeholder: Optional[str] = None
    required: bool
    options: Optional[List[str]] = None
    subfields: Optional[List[Dict]] = None

class FunctionSchema(BaseModel):
    name: str
    fields: List[FunctionField]
    endpoint: str
