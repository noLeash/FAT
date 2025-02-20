from typing import Optional, List
from pydantic import BaseModel, Field

# Define Pydantic model for dropdown items with self-referencing
class DropdownItem(BaseModel):
    id: int
    title: str
    children: Optional[List["DropdownItem"]] = Field(default=None)
    method: Optional[str] = Field(default=None)

    # ✅ This is required in Pydantic v2 for self-referencing models
    model_config = {
        "arbitrary_types_allowed": True
    }

# ✅ This replaces update_forward_refs() in Pydantic v2
DropdownItem.model_rebuild()





