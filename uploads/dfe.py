# ml_model.py
import joblib
from transformers import AutoTokenizer, AutoModelForSequenceClassification

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSequenceClassification.from_pretrained("your_fine_tuned_model")

def predict_issue(issue):
    """
    issue: dict with keys like {'analyzer':..., 'message':..., 'code':...}
    """
    text = issue["message"] + " " + issue.get("code", "")
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    outputs = model(**inputs)
    probs = outputs.logits.softmax(dim=-1)
    severity_id = probs.argmax(dim=-1).item()

    severity_map = {0: "low", 1: "medium", 2: "high"}
    severity = severity_map[severity_id]
    suggestion = generate_suggestion(issue, severity)
    return {"predicted_severity": severity, "suggestion": suggestion}

def generate_suggestion(issue, severity):
    # Could use a second fine-tuned model or a rule-based template
    return f"{severity.capitalize()} issue detected: consider refactor, add tests, or security fix."
