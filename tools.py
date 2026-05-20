from pathlib import Path
from typing import Dict, List
import re


ALLOWED_EXTENSIONS = {
    ".py", ".js", ".ts", ".tsx", ".jsx", ".java", ".go", ".rs",
    ".md", ".txt", ".yml", ".yaml", ".json", ".toml", ".ini",
    ".sql", ".html", ".css", ".scss"
}

IGNORE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "__pycache__",
    "dist", "build", ".next", ".idea", ".vscode"
}


def collect_repo_files(repo_path: str, max_files: int = 80) -> Dict[str, str]:
    """Read important source files from a repository."""
    root = Path(repo_path).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Invalid repo_path: {repo_path}")

    collected: Dict[str, str] = {}

    for file_path in root.rglob("*"):
        if len(collected) >= max_files:
            break

        if any(part in IGNORE_DIRS for part in file_path.parts):
            continue

        if file_path.is_file():
            suffix = file_path.suffix.lower()
            if suffix in ALLOWED_EXTENSIONS or file_path.name.lower() in {"dockerfile", "makefile"}:
                try:
                    rel = str(file_path.relative_to(root))
                    content = file_path.read_text(encoding="utf-8", errors="ignore")
                    collected[rel] = content[:6000]
                except Exception:
                    continue

    return collected


def detect_tech_stack(files: Dict[str, str]) -> List[str]:
    """Simple rule-based tech stack detector."""
    stack = set()
    names = " ".join(files.keys()).lower()
    content = "\n".join(files.values()).lower()
    text = names + "\n" + content

    checks = {
        "Python": [".py", "requirements.txt", "pyproject.toml"],
        "FastAPI": ["fastapi", "uvicorn"],
        "Flask": ["flask"],
        "Django": ["django"],
        "Angular": ["angular.json", "@angular/core"],
        "React": ["react", "vite", "next"],
        "TypeScript": [".ts", ".tsx", "typescript"],
        "SQLAlchemy": ["sqlalchemy"],
        "Pydantic": ["pydantic"],
        "Docker": ["dockerfile", "docker-compose"],
        "AWS": ["boto3", "lambda", "s3", "cloudwatch", "ecs"],
        "PostgreSQL": ["postgres", "psycopg"],
        "MySQL": ["mysql"],
        "Redis": ["redis"],
        "OpenAI": ["openai"],
        "LangChain": ["langchain"],
        "Pytest": ["pytest"],
        "GitHub Actions": [".github/workflows"],
    }

    for tech, patterns in checks.items():
        if any(pattern in text for pattern in patterns):
            stack.add(tech)

    return sorted(stack)


def scan_security_risks(files: Dict[str, str]) -> List[str]:
    """Find obvious secrets and risky patterns."""
    findings = []
    secret_patterns = [
        r"AKIA[0-9A-Z]{16}",
        r"(?i)aws_secret_access_key\s*=\s*['\"][^'\"]+",
        r"(?i)api[_-]?key\s*=\s*['\"][^'\"]+",
        r"(?i)password\s*=\s*['\"][^'\"]+",
        r"(?i)secret\s*=\s*['\"][^'\"]+",
    ]

    for path, content in files.items():
        for pattern in secret_patterns:
            if re.search(pattern, content):
                findings.append(f"Potential secret or credential found in {path}")

        if "allow_origins=[\"*\"]" in content.replace(" ", ""):
            findings.append(f"Open CORS policy detected in {path}")

        if "debug=True" in content.replace(" ", ""):
            findings.append(f"Debug mode enabled in {path}")

    return sorted(set(findings))


def architecture_notes(files: Dict[str, str], tech_stack: List[str]) -> List[str]:
    notes = []

    if "FastAPI" in tech_stack:
        notes.append("Backend appears to expose REST APIs using FastAPI.")
    if "SQLAlchemy" in tech_stack:
        notes.append("Application uses SQLAlchemy ORM/data access patterns.")
    if "Docker" in tech_stack:
        notes.append("Docker support is present, useful for containerized deployment.")
    if "GitHub Actions" in tech_stack:
        notes.append("CI/CD workflow exists through GitHub Actions.")
    if "OpenAI" in tech_stack or "LangChain" in tech_stack:
        notes.append("AI/LLM integration is present, suitable for GenAI workflows.")
    if not notes:
        notes.append("Architecture is unclear from detected files; add README architecture section.")

    return notes


def readme_suggestions(files: Dict[str, str]) -> List[str]:
    has_readme = any(path.lower() == "readme.md" for path in files)
    suggestions = []

    if not has_readme:
        suggestions.append("Add a README.md with project overview, setup, API examples, and architecture.")
    else:
        readme = files.get("README.md") or files.get("readme.md") or ""
        if "architecture" not in readme.lower():
            suggestions.append("Add an Architecture section with request flow and major components.")
        if "setup" not in readme.lower() and "install" not in readme.lower():
            suggestions.append("Add setup/install instructions.")
        if "api" not in readme.lower():
            suggestions.append("Add API usage examples.")
        if "test" not in readme.lower():
            suggestions.append("Add testing instructions.")

    return suggestions or ["README looks reasonably complete."]
