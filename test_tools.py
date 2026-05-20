from app.tools import detect_tech_stack, scan_security_risks


def test_detect_fastapi_stack():
    files = {
        "main.py": "from fastapi import FastAPI\nfrom pydantic import BaseModel",
        "requirements.txt": "fastapi\nuvicorn\npydantic"
    }
    stack = detect_tech_stack(files)
    assert "FastAPI" in stack
    assert "Pydantic" in stack
    assert "Python" in stack


def test_security_scan_detects_password():
    files = {
        "config.py": "password = 'hardcoded-password'"
    }
    findings = scan_security_risks(files)
    assert len(findings) > 0
