import os
import shutil
import tempfile
from flask import Flask, request, render_template, session
from analyzers import analyze_file
from ml_model import predict_issue
from git import Repo

UPLOAD_FOLDER = "uploads"
# Ensure the uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.secret_key = "your_secure_random_key"  # IMPORTANT: Change this to a secure key


# Landing page
@app.route("/")
def home():
    return render_template("home.html")


# Code input page (form)
@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        code = request.form.get("code")
        filename = request.form.get("filename")
        repo_url = request.form.get("repo_url")
        uploaded_files = request.files.getlist("files")

        issues = []
        full_code_display = "" # Holds the code for display in results.html

        # --- Case 1: GitHub repo provided (Corrected Logic) ---
        if repo_url:
            temp_dir = tempfile.mkdtemp()
            try:
                Repo.clone_from(repo_url, temp_dir)
                repo_name = repo_url.split("/")[-1]
                filename = repo_name # Use repo name as the main filename display

                # 1. Iterate over all relevant files in the cloned repo
                for root, _, files in os.walk(temp_dir):
                    for f in files:
                        if f.endswith((".py", ".c", ".cpp", ".h")):
                            file_path = os.path.join(root, f)
                            
                            # Read the file content for display
                            with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                                file_content = file.read()
                                # Add file path to code display for context
                                full_code_display += f"\n\n# ===== {os.path.join(repo_name, os.path.relpath(file_path, temp_dir))} =====\n" + file_content
                                
                            # 2. Run analyzer on the individual file (correct extension)
                            file_issues = analyze_file(file_path)

                            # 3. Add file context to each issue
                            for issue in file_issues:
                                # Add 'source_file' key to each issue for display
                                issue["source_file"] = os.path.join(os.path.basename(root), f)
                                issues.append(issue)

            finally:
                # Always clean up the temporary directory
                shutil.rmtree(temp_dir)
                
            code = full_code_display # Set the aggregated code for display

        # --- Case 2: File upload ---
        elif uploaded_files and uploaded_files[0].filename:
            file = uploaded_files[0]
            filename = file.filename
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)
            
            with open(save_path, "r", encoding="utf-8", errors="ignore") as f:
                code = f.read()
            
            # Run analyzer on the saved file
            issues = analyze_file(save_path)

        # --- Case 3: Manual paste ---
        elif code and filename:
            clean_code = code.replace("\r", "").replace("\uFEFF", "").lstrip("\n")
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            with open(save_path, "w", encoding="utf-8") as f:
                f.write(clean_code)
                
            code = clean_code # Use the cleaned code for display
            
            # Run analyzer on the saved file
            issues = analyze_file(save_path)

        else:
            return "You must provide code, upload a file, or give a repo URL", 400

        # --- Run ML Prediction and Calculate Score ---
        severity_weights = {"high": 3, "medium": 2, "low": 1, "none": 0}
        total_weight = 0
        
        # Process all collected issues (from repo or single file)
        for it in issues:
            res = predict_issue(it)
            it["predicted_severity"] = res["predicted_severity"]
            it["suggestion"] = res["suggestion"]
            total_weight += severity_weights.get(res["predicted_severity"].lower(), 0)

        # Calculate score (capped at 100)
        score = max(0, 100 - total_weight * 5)

        return render_template("results.html",
                               filename=filename,
                               issues=issues,
                               score=score,
                               code=code)

    return render_template("index.html", code="", filename="")


if __name__ == "__main__":
    app.run(debug=True, port=5001)