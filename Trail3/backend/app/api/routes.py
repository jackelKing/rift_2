from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
from app.core.orchestrator import run_analysis

router = APIRouter()


@router.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    required = [
        "transaction_id",
        "sender_id",
        "receiver_id",
        "amount",
        "timestamp"
    ]

    if not all(col in df.columns for col in required):
        raise HTTPException(status_code=400, detail="Invalid CSV structure")

    return run_analysis(df)
