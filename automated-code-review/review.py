# review.py
import sys, os, json
from analyzers import analyze_file
from ml_model import predict_issue

def review_path(path):
    results = []
    if os.path.isdir(path):
        for root, dirs, files in os.walk(path):
            for fn in files:
                if fn.endswith((".py", ".cpp", ".cc", ".c", ".h", ".hpp")):
                    fp = os.path.join(root, fn)
                    issues = analyze_file(fp)
                    for it in issues:
                        res = predict_issue(it)
                        it["predicted_severity"] = res["predicted_severity"]
                        it["suggestion"] = res["suggestion"]
                    results.extend(issues)
    elif os.path.isfile(path):
        issues = analyze_file(path)
        for it in issues:
            res = predict_issue(it)
            it["predicted_severity"] = res["predicted_severity"]
            it["suggestion"] = res["suggestion"]
        results = issues
    else:
        print("Path not found:", path)
        return
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python review.py <file_or_directory>")
    else:
        review_path(sys.argv[1])
