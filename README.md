# Repo Intelligence Agent

A recruiter-friendly AI agent project that analyzes any GitHub repository or local code folder and produces:

- Tech stack summary
- Architecture explanation
- README improvement suggestions
- Security red-flag scan
- Code quality observations
- Interview-ready project explanation
- Optional AI-generated answer using OpenAI

## Why this project is trending

AI agents are moving beyond chatbots. The strongest portfolio projects now show an agent that can read files, use tools, reason over code, and produce useful engineering outputs.

## Architecture

```text
User
  ↓
FastAPI API
  ↓
Repo Intelligence Agent
  ↓
Tools:
  - File reader
  - Tech stack detector
  - Security scanner
  - README analyzer
  - Prompt builder
  ↓
OpenAI LLM optional
  ↓
Structured JSON response
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- Async APIs
- OpenAI API optional
- Pytest

## Setup

```powershell
git clone <your-repo-url>
cd repo-intelligence-agent
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Add your OpenAI key in `.env` if you want LLM output:

```text
OPENAI_API_KEY=your_key_here
```

The project also works without OpenAI using rule-based fallback analysis.

## Run API

```powershell
uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

## Example API Request

POST `/analyze`

```json
{
  "repo_path": "C:/projects/my-fastapi-app",
  "question": "Explain this project like I am in an interview"
}
```

## Run Tests

```powershell
pytest
```

## GitHub Push Commands

```powershell
git init
git add .
git commit -m "Initial commit: repo intelligence agent"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/repo-intelligence-agent.git
git push -u origin main
```
