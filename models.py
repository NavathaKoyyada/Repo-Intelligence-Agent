from pydantic import BaseModel, Field
from typing import List, Optional


class AnalyzeRequest(BaseModel):
    repo_path: str = Field(..., description="Local repository folder path")
    question: Optional[str] = Field(
        default="Explain this project like I am in an interview",
        description="User question for the agent"
    )


class AnalyzeResponse(BaseModel):
    summary: str
    tech_stack: List[str]
    security_findings: List[str]
    architecture_notes: List[str]
    readme_suggestions: List[str]
    interview_pitch: str
