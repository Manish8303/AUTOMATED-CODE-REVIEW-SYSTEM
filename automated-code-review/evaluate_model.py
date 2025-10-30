# evaluate_model.py
"""
Script to evaluate the accuracy and developer acceptance of ML suggestions
using open-source code files (e.g., from GitHub datasets).

Usage:
    python evaluate_model.py <code_issues.csv>

The CSV should have columns: message, code, true_severity
"""
import pandas as pd
import joblib
from sklearn.metrics import classification_report, accuracy_score
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml_severity_model.joblib")
model = joblib.load(MODEL_PATH)

def evaluate(csv_path):
    df = pd.read_csv(csv_path)
    X = (df["message"] + " " + df["code"]).fillna("")
    y_true = df["true_severity"]
    y_pred = model.predict(X)
    print("Accuracy:", accuracy_score(y_true, y_pred))
    print("Classification Report:")
    print(classification_report(y_true, y_pred))

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python evaluate_model.py <code_issues.csv>")
    else:
        evaluate(sys.argv[1])
