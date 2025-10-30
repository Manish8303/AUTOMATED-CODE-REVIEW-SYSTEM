# ml_model.py
import re
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer
from sklearn.preprocessing import LabelEncoder

# We'll train a tiny synthetic dataset on startup (demonstration).
# In production you'd replace this with a real dataset from previous lint fixes.

SYNTHETIC_SAMPLES = [
    # analyzer, keywords, severity (high/medium/low)
    ("bandit", "shell subprocess eval os.system", "high"),
    ("bandit", "pickle insecure", "high"),
    ("pylint", "unused-variable", "low"),
    ("pylint", "line-too-long", "low"),
    ("pylint", "too-many-branches complexity", "medium"),
    ("cpplint", "whitespace/end_of_line", "low"),
    ("cpplint", "runtime/printf", "medium"),
    ("pylint", "unused-argument", "low"),
    ("bandit", "assert used", "medium"),
    ("pylint", "dangerous-default-value", "medium"),
    ("bandit", "hardcoded_password", "high"),
    ("cpplint", "build/include_order", "low"),
    ("pylint", "redefined-outer-name", "medium"),
    ("pylint", "too-many-lines", "medium"),
    ("bandit", "insecure-hash", "high"),
]

def extract_features_from_issue(issue):
    """
    Convert an issue dict into feature dict used by the classifier.
    """
    msg = (issue.get("message") or str(issue.get("raw") or "")).lower()
    analyzer = issue.get("analyzer", "unknown")
    features = {
        "analyzer": analyzer,
        "msg_len": len(msg),
        "has_unused": "unused" in msg,
        "has_shell": any(k in msg for k in ["subprocess", "shell", "os.system", "popen", "eval"]),
        "has_security": any(k in msg for k in ["password", "secret", "insecure", "pickle", "hash", "crypto"]),
        "has_complexity": any(k in msg for k in ["complex", "too-many", "mccabe", "cyclomatic"]),
        "has_line_len": "line-too-long" in msg or "line length" in msg,
    }
    return features

# train tiny model
def train_small_model():
    X = []
    y = []
    for analyzer, keywords, sev in SYNTHETIC_SAMPLES:
        feat = {
            "analyzer": analyzer,
            "msg_len": len(keywords),
            "has_unused": "unused" in keywords,
            "has_shell": any(k in keywords for k in ["subprocess", "shell", "os.system", "eval"]),
            "has_security": any(k in keywords for k in ["password", "secret", "insecure", "pickle", "hash"]),
            "has_complexity": "complex" in keywords or "too-many" in keywords,
            "has_line_len": "line-too-long" in keywords,
        }
        X.append(feat)
        y.append(sev)
    dv = DictVectorizer(sparse=False)
    Xvec = dv.fit_transform(X)
    le = LabelEncoder()
    yenc = le.fit_transform(y)
    clf = RandomForestClassifier(n_estimators=40, random_state=42)
    clf.fit(Xvec, yenc)
    return {"dv": dv, "clf": clf, "le": le}

_MODEL = train_small_model()

SUGGESTION_TEMPLATES = [
    # (matcher_fn, suggestion_text, severity_hint)
    (lambda i: i.get("analyzer") == "bandit" and any(k in (i.get("message") or "").lower() for k in ["subprocess","shell","popen","os.system","eval"]),
     "Security risk: avoid invoking shell or eval on untrusted input. Use subprocess.run with a list of args, validate/escape inputs, or use shlex.split. Example:\n\nsubprocess.run(['ls','-la'])\n\nDo input validation and avoid concatenating strings to make commands.",
     "high"),
    (lambda i: "unused" in (i.get("message") or "").lower(),
     "Code smell: remove unused variables or prefix them with underscore `_` if intentionally unused. This reduces confusion and improves readability.",
     "low"),
    (lambda i: any(k in (i.get("message") or "").lower() for k in ["too-many", "complex", "mccabe"]),
     "Refactor suggestion: function is too complex. Split into smaller functions, reduce branching and nested loops. Consider adding unit tests for critical paths.",
     "medium"),
    (lambda i: "line-too-long" in (i.get("message") or "").lower() or len((i.get("message") or "")) > 120,
     "Style: wrap long lines to < 80/100 chars and consider configuring a code formatter (black for Python, clang-format for C++).",
     "low"),
    (lambda i: "hardcoded_password" in (i.get("message") or "").lower() or "password" in (i.get("message") or "").lower(),
     "Security: do not hardcode credentials. Use environment variables or a secrets manager. Rotate secrets and use strong hashing.",
     "high"),
]

def predict_issue(issue):
    feat = extract_features_from_issue(issue)
    dv = _MODEL["dv"]
    clf = _MODEL["clf"]
    le = _MODEL["le"]
    Xvec = dv.transform([feat])
    ypred = clf.predict(Xvec)[0]
    severity = le.inverse_transform([ypred])[0]
    # map to suggestion via templates (first match)
    suggestion = None
    for matcher, text, hint in SUGGESTION_TEMPLATES:
        try:
            if matcher(issue):
                suggestion = text
                break
        except Exception:
            continue
    if suggestion is None:
        # generic suggestions based on severity
        if severity == "high":
            suggestion = "High priority: investigate security and correctness. If this is security-related, fix ASAP. Provide unit tests and input sanitization."
        elif severity == "medium":
            suggestion = "Medium: consider refactor or further review. Add tests and/or refactor to improve maintainability."
        else:
            suggestion = "Low: style or minor issue. Apply formatter and fix minor issues when convenient."
    return {"predicted_severity": severity, "suggestion": suggestion}
