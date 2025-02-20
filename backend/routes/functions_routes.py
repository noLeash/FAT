import json
from fastapi import APIRouter, HTTPException
from pathlib import Path
from typing import List
from models.react_models import DropdownItem


router = APIRouter()




# Sample data for menu
menu_data = [
    DropdownItem(
        id=1,
        title="Item 1"
    ),
    DropdownItem(
        id=2,
        title="Item 2",
        children=[
            DropdownItem(
                id=21,
                title="Item 2-1",
                children=[
                    DropdownItem(id=211, title="Item 2-1-1"),
                    DropdownItem(id=212, title="Item 2-1-2"),
                    DropdownItem(id=213, title="Item 2-1-3")
                ]
            ),
            DropdownItem(id=22, title="Item 2-2"),
            DropdownItem(id=23, title="Item 2-3"),
        ]
    ),
    DropdownItem(
        id=3,
        title="Item 3",
        children=[
            DropdownItem(id=31, title="Item 3-1"),
            DropdownItem(id=32, title="Item 3-2"),
        ]
    )
]

# Load function dictionary from JSON file
FUNCTIONS_FILE = Path("routes/function_dictionary.json")


# Recursive function to convert JSON to Pydantic models
def parse_dropdown_items(data) -> List[DropdownItem]:
    menu_items = []
    
    for item in data:
        if "id" not in item or "type" not in item or "method" not in item:  # Ensure required fields exist
            print(f"⚠️ Skipping invalid item: {item}")
            continue  # Skip items with missing keys

        # Recursively parse children if present
        children = parse_dropdown_items(item.get("children", [])) if "children" in item else None

        menu_items.append(DropdownItem(
            id=item["id"],
            title=item["type"],  # Mapping 'type' to 'title'
            children=children,
            method=item["method"] if item["method"] is not None else None
        ))

    print(menu_items)
    return menu_items


def load_functions():
    print(f"load_functions() init")
    try:
        print(f"load_functions() init")
        with open(FUNCTIONS_FILE, "r", encoding="utf-8") as file:
            json_data = json.load(file)
            for item in json_data:
                print(f"\nItem: {item['type']}\n")
            dropdown_functions = parse_dropdown_items(json_data)
            return dropdown_functions
        
    except json.JSONDecodeError as e:
        print(f"Error loading JSON: {e}")
        return []  # ✅ Return empty list on failure
    
    except FileNotFoundError:
        print("Error: JSON file not found.")
        return []  # ✅ Return empty list if file is missing
        
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=f"Error loading function dictionary: {str(e)}")









# Endpoint to return menu items
@router.get("/listof", response_model=List[DropdownItem])
async def get_menu_items() -> DropdownItem:
    
    return load_functions()






