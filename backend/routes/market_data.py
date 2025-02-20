from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload-csv")
def upload_csv(file: UploadFile = File(...)):
    return {"status": "success", "filename": file.filename}

@router.get("/market-data")
def get_market_data(symbol: str, start_date: str, end_date: str):
    mock_data = {
        "symbol": symbol,
        "data": [
            {"date": start_date, "price": 100.0},
            {"date": end_date, "price": 105.0}
        ]
    }
    return mock_data
