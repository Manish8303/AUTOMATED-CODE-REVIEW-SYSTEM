

# ml_model.py
import joblib
import os

# Load the trained ML model (scikit-learn pipeline)
MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_severity_model.joblib")
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None

def predict_issue(issue):
    message = issue.get("message", "").strip().lower()
    # Treat non-critical style warnings and non-printable character warnings as 'no issues'
    ignore_patterns = [
        "invalid non-printable character u+000d",
        "trailing whitespace",
        "line ends in whitespace",
        "missing newline",
        "line too long",
        "minor style",
        "convention",
        "minor",
        "suggestion",
        "copyright message"
    ]
    if (
        not message or
        message in ["no issues found.", "no issues", "", None] or
        any(pat in message for pat in ignore_patterns)
    ):
        return {
            "predicted_severity": "None",
            "suggestion": "Your code looks good! No issues detected. Keep following best practices."
        }

    # Use the ML model if available
    text = (issue.get("message", "") + " " + issue.get("code", "")).lower()
    if model:
        severity = model.predict([text])[0]
    else:
        # fallback: rule-based
        if any(w in text for w in ["security", "vulnerability", "danger", "injection", "buffer overflow"]):
            severity = "high"
        elif any(w in text for w in ["warning", "deprecated", "bad practice", "should", "could"]):
            severity = "medium"
        else:
            severity = "low"
    suggestion = generate_suggestion(issue, severity)
    return {"predicted_severity": severity, "suggestion": suggestion}

def generate_suggestion(issue, severity):
    message = issue.get("message", "").lower()
    # Rule-based actionable suggestions for common issues
    if "eval" in message:
        return "Avoid using eval(). Use safer alternatives like ast.literal_eval() for parsing literals."
    if "input validation" in message or "unsanitized" in message:
        return "Add input validation and sanitize all user inputs to prevent security vulnerabilities."
    if "deprecated" in message:
        return "Replace deprecated functions with their recommended alternatives."
    if "snake_case" in message:
        return "Rename variables and functions to use snake_case for better readability."
    if "line too long" in message:
        return "Break long lines into shorter ones to comply with style guidelines (PEP8: max 79 chars)."
    if "missing docstring" in message:
        return "Add a docstring to describe the purpose and usage of this function/class/module."
    if "bad practice" in message:
        return "Refactor code to follow best practices and improve maintainability."
    if "security" in message:
        return "Address security vulnerabilities immediately. Sanitize inputs, validate data, and avoid unsafe functions."
    if "buffer overflow" in message:
        return "Check array bounds and use safe functions to prevent buffer overflows."
    if "line ends in whitespace" in message or "trailing whitespace" in message:
        return "Remove trailing whitespace from the end of the line."
    if "missing newline" in message:
        return "Add a newline at the end of the file."
    if "variable name not descriptive" in message:
        return "Rename variables to be more descriptive."
    if "no issues" in message or severity == "none":
        return "Your code looks good! No issues detected. Keep following best practices."
    # Fallbacks for severity
    if severity == "high":
        return "High severity: Critical issue. Refactor code, add security checks, and write tests."
    elif severity == "medium":
        return "Medium severity: Consider refactoring, improving code readability, or updating deprecated usage."
    elif severity == "low":
        return "Low severity: Minor style or convention issue. Clean up formatting or follow style guidelines."
    else:
        return "No issues detected."
