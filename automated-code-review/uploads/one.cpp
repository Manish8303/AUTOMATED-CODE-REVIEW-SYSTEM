# analyzers.py
import subprocess, json, re
from pathlib import Path

def run_pylint(filepath: str):
    cmd = ["pylint", "--output-format=json", filepath]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    issues = []
    try:
        data = json.loads(proc.stdout.strip() or "[]")
        for item in data:
            issues.append({
                "analyzer": "pylint",
                "file": item.get("path", filepath),
                "line": item.get("line", 0),
                "message": item.get("message", ""),
                "symbol": item.get("symbol", ""),
                "message_id": item.get("message-id", ""),
                "raw": item
            })
    except Exception:
        pass
    return issues

def run_bandit(filepath: str):
    cmd = ["bandit", "-r", filepath, "-f", "json"]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    issues = []
    try:
        data = json.loads(proc.stdout.strip() or "{}")
        for res in data.get("results", []):
            issues.append({
                "analyzer": "bandit",
                "file": res.get("filename", filepath),
                "line": res.get("line_number", 0),
                "message": res.get("issue_text", ""),
                "test_name": res.get("test_name", ""),
                "issue_severity": res.get("issue_severity", ""),
                "raw": res
            })
    except Exception:
        pass
    return issues

def run_cpplint(filepath: str):
    cmd = ["cpplint", filepath]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    out = proc.stderr.strip()
    issues = []
    if not out:
        return issues
    for line in out.splitlines():
        m = re.match(r"^(.*?):(\d+):\s*(.*?)\s+\[(.*?)\]\s+\[(\d+)\]$", line.strip())
        if m:
            filename, lineno, msg, category, severity = m.groups()
            issues.append({
                "analyzer": "cpplint",
                "file": filename,
                "line": int(lineno),
                "message": msg,
                "category": category,
                "severity": int(severity),
                "raw": line.strip()
            })
        else:
            issues.append({
                "analyzer": "cpplint",
                "file": filepath,
                "line": 0,
                "message": line.strip(),
                "raw": line.strip()
            })
    return issues

def run_cppcheck(filepath: str):
    """
    Runs cppcheck to catch real C++ issues, memory leaks, and warnings.
    Captures JSON from stderr and falls back to raw lines if needed.
    """
    cmd = ["cppcheck", "--enable=all", "--template=json", filepath]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)

    output = proc.stderr.strip() or proc.stdout.strip()
    issues = []

    try:
        data = json.loads(output) if output else {}
        for msg in data.get("messages", []):
            issues.append({
                "analyzer": "cppcheck",
                "file": msg.get("file", filepath),
                "line": msg.get("line", 0),
                "message": msg.get("message", ""),
                "severity": msg.get("severity", ""),
                "id": msg.get("id", ""),
                "raw": msg
            })
    except Exception:
        # fallback: parse raw lines
        for line in output.splitlines():
            issues.append({
                "analyzer": "cppcheck",
                "file": filepath,
                "line": 0,
                "message": line.strip(),
                "raw": line.strip()
            })

    return issues

def analyze_file(filepath: str):
    p = Path(filepath)
    ext = p.suffix.lower()
    results = []
    if ext == ".py":
        results += run_pylint(filepath)
        results += run_bandit(filepath)
    else:
        results += run_cpplint(filepath)
        results += run_cppcheck(filepath)
    return results
