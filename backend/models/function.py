from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import datetime as dt

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

