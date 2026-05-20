import os
from typing import Dict, List
from dotenv import load_dotenv
from openai import OpenAI

from app.tools import (
    collect_repo_files,
    detect_tech_stack,
    scan_security_risks,
    architecture_notes,
    readme_suggestions,
)

load_dotenv()


def build_context(files: Dict[str, str], max_chars: int = 18000) -> str:
    chunks = []
    total = 0

    for path, content in files.items():
        block = f"\n--- FILE: {path} ---\n{content[:2500]}"
        if total + len(block) > max_chars:
            break
        chunks.append(block)
        total += len(block)

    return "\n".join(chunks)


def fallback_interview_pitch(tech_stack: List[str], notes: List[str]) -> str:
    stack = ", ".join(tech_stack) if tech_stack else "modern backend technologies"
    return (
        f"This project demonstrates a practical engineering agent that analyzes code repositories "
        f"using {stack}. It reads source files, detects the technology stack, checks security risks, "
        f"reviews documentation, and generates architecture insights. The design shows backend API "
        f"development, tool-based agent reasoning, clean code organization, and production-readiness."
    )


def ask_llm(question: str, files: Dict[str, str], tech_stack: List[str], findings: List[str]) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("MODEL_NAME", "gpt-4o-mini")

    if not api_key:
        return ""

    client = OpenAI(api_key=api_key)
    context = build_context(files)

    prompt = f"""
You are a senior software architect and AI agent reviewer.

User question:
{question}

Detected tech stack:
{tech_stack}

Security findings:
{findings}

Repository context:
{context}

Give a crisp, recruiter-friendly, technically accurate answer.
Focus on architecture, backend quality, security, scalability, and interview explanation.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a concise senior AI/software architect."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content or ""


def analyze_repository(repo_path: str, question: str) -> dict:
    files = collect_repo_files(repo_path)
    stack = detect_tech_stack(files)
    findings = scan_security_risks(files)
    notes = architecture_notes(files, stack)
    suggestions = readme_suggestions(files)

    llm_answer = ask_llm(question, files, stack, findings)
    pitch = llm_answer or fallback_interview_pitch(stack, notes)

    summary = (
        f"Analyzed {len(files)} repository files. "
        f"Detected technologies: {', '.join(stack) if stack else 'not enough evidence'}."
    )

    return {
        "summary": summary,
        "tech_stack": stack,
        "security_findings": findings,
        "architecture_notes": notes,
        "readme_suggestions": suggestions,
        "interview_pitch": pitch,
    }
