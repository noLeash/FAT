from pydantic import BaseModel
from typing import List, Dict, Optional, Any
import datetime as dt



class ibBars(BaseModel):
    ticker: str = None
    start: dt.datetime = None
    end: dt.datetime = None
    duration: dt.timedelta = None
    bar_size: str = "1 D" 
    bars: list[Any] = []

class tick(BaseModel):
    open: float = None
    high: float = None
    low: float = None
    close: float = None
    volume: float = None
    time: float = None