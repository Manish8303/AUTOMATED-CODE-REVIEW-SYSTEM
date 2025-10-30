# train_ml_model.py
# Example: Train a simple ML model for code issue severity prediction

import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split

# Example data: (In practice, use a larger, labeled dataset)
data = [
    ("use of eval is dangerous", "high"),
    ("missing input validation", "high"),
    ("deprecated function used", "medium"),
    ("should use snake_case", "low"),
    ("line too long", "low"),
    ("no issues found", "none"),
    ("buffer overflow possible", "high"),
    ("variable name not descriptive", "low"),
    ("security vulnerability detected", "high"),
    ("missing docstring", "low"),
    ("bad practice", "medium"),
]

X, y = zip(*data)

# Split for demonstration (not needed for real use if you have a full dataset)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", RandomForestClassifier(n_estimators=50, random_state=42)),
])

pipeline.fit(X_train, y_train)

# Save the model
joblib.dump(pipeline, "ml_severity_model.joblib")

print("Model trained and saved as ml_severity_model.joblib")
