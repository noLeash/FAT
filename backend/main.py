from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File, HTTPException
from routes import functions_routes, methods_routes
from typing import Optional, List
from pydantic import BaseModel, Field
from utils.logger import setup_logging

app = FastAPI()
logger = setup_logging()

# Include function-related and market data routes
app.include_router(functions_routes.router, prefix="/functions")
app.include_router(methods_routes.methods_routes, prefix="/api")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, restrict to frontend if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "Welcome to the Finance Function API"}


@app.get("/api/data")
def home():
    return {"message": "Welcome to the Finance Function API"}



