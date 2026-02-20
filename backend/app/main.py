from app.core.database import Base, engine

# IMPORT MODELS BEFORE create_all
from app.models import db_models

Base.metadata.create_all(bind=engine)

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import asyncio

from app.core.orchestrator import run_analysis

app = FastAPI(
    title="RIFT 2026 – Money Muling Detection Engine",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "RIFT 2026 Financial Crime Detection Engine is running."
    }


@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a valid CSV file.")

    content = await file.read()

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format.")

    # Run blocking computation in separate thread
    try:
        results = await asyncio.to_thread(run_analysis, df)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return results


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8023,
        reload=True
    )
