from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
from app.core.orchestrator import run_analysis

app = FastAPI()

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_data(file: UploadFile = File(...)):
    # Read CSV
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    
    # Run Orchestrator
    results = run_analysis(df)
    
    return results

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)