import subprocess, json, re
from pathlib import Path

def safe_run(cmd):
    """Run subprocess safely and always return output."""
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        return proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return "", f"[subprocess error: {e}]"

# -------------------- PYTHON ANALYZERS --------------------

def run_pylint(filepath: str):
    cmd = ["pylint", "--output-format=json", filepath]
    stdout, stderr = safe_run(cmd)
    issues = []

    try:
        data = json.loads(stdout or "[]")
        for item in data:
            issues.append({
                "analyzer": "pylint",
                "file": item.get("path", filepath),
                "line": item.get("line", 0),
                "message": item.get("message", ""),
                "symbol": item.get("symbol", ""),
                "message_id": item.get("message-id", ""),
                "severity": "low",
                "raw": item
            })
    except json.JSONDecodeError:
        # Fallback: parse stderr for syntax errors
        for line in (stderr or stdout).splitlines():
            if "error" in line.lower() or "fatal" in line.lower():
                issues.append({
                    "analyzer": "pylint",
                    "file": filepath,
                    "line": 0,
                    "message": line.strip(),
                    "severity": "high",
                    "raw": line.strip()
                })
    return issues


def run_bandit(filepath: str):
    cmd = ["bandit", "-r", filepath, "-f", "json"]
    stdout, stderr = safe_run(cmd)
    issues = []
    try:
        data = json.loads(stdout or "{}")
        for res in data.get("results", []):
            issues.append({
                "analyzer": "bandit",
                "file": res.get("filename", filepath),
                "line": res.get("line_number", 0),
                "message": res.get("issue_text", ""),
                "test_name": res.get("test_name", ""),
                "issue_severity": res.get("issue_severity", "MEDIUM"),
                "raw": res
            })
    except Exception:
        for line in (stderr or stdout).splitlines():
            issues.append({
                "analyzer": "bandit",
                "file": filepath,
                "line": 0,
                "message": line.strip(),
                "raw": line.strip()
            })
    return issues

# -------------------- C / C++ ANALYZERS --------------------

def run_cpplint(filepath: str):
    cmd = ["cpplint", filepath]
    _, stderr = safe_run(cmd)
    out = stderr.strip()
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
    cmd = ["cppcheck", "--enable=all", "--template=json", filepath]
    _, stderr = safe_run(cmd)
    output = stderr.strip()
    issues = []
    try:
        data = json.loads(output or "{}")
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
        for line in output.splitlines():
            issues.append({
                "analyzer": "cppcheck",
                "file": filepath,
                "line": 0,
                "message": line.strip(),
                "raw": line.strip()
            })
    return issues


def run_gpp(filepath: str):
    cmd = ["g++", "-fsyntax-only", filepath]
    _, stderr = safe_run(cmd)
    output = stderr.strip()
    issues = []
    for line in output.splitlines():
        m = re.match(r"^(.*?):(\d+):(?:(\d+):)?\s*(error|warning):\s*(.*)$", line)
        if m:
            filename, lineno, col, typ, msg = m.groups()
            issues.append({
                "analyzer": "g++",
                "file": filename,
                "line": int(lineno),
                "type": typ,
                "message": msg,
                "raw": line
            })
        else:
            issues.append({
                "analyzer": "g++",
                "file": filepath,
                "line": 0,
                "type": "error",
                "message": line,
                "raw": line
            })
    return issues

# -------------------- MAIN ROUTER --------------------

def analyze_file(filepath: str):
    """
    Runs syntax check first, then analyzers (so you get ALL issues even if code doesn't compile).
    """
    p = Path(filepath)
    ext = p.suffix.lower()
    results = []

    # --- Python Files ---
    if ext == ".py":
        # 1️⃣ Run syntax validation first
        syntax_cmd = ["python", "-m", "py_compile", filepath]
        proc = subprocess.run(syntax_cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            # Add syntax errors as high-severity issues
            for line in (proc.stderr.strip().splitlines() or []):
                results.append({
                    "analyzer": "python-syntax",
                    "file": filepath,
                    "line": 0,
                    "message": line.strip(),
                    "severity": "high"
                })

        # 2️⃣ Run Pylint & Bandit regardless of syntax
        results += run_pylint(filepath)
        results += run_bandit(filepath)

    # --- C/C++ Files ---
    elif ext in [".c", ".cpp", ".cc", ".h", ".hpp"]:
        results += run_cpplint(filepath)
        results += run_cppcheck(filepath)
        results += run_gpp(filepath)

    else:
        results.append({
            "analyzer": "system",
            "file": filepath,
            "message": f"Unsupported file extension: {ext}",
            "severity": "info"
        })

    return results
