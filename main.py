from fastapi import FastAPI, HTTPException
from app.models import AnalyzeRequest, AnalyzeResponse
from app.agent import analyze_repository

app = FastAPI(
    title="Repo Intelligence Agent",
    description="AI agent that analyzes GitHub/local repositories and generates engineering insights.",
    version="1.0.0",
)


@app.get("/")
async def health_check():
    return {"status": "ok", "message": "Repo Intelligence Agent is running"}


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest):
    try:
        result = analyze_repository(request.repo_path, request.question or "")
        return result
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
