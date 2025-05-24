from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import sys
import json
from datetime import datetime
import subprocess

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Angular dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure paths
UPLOAD_DIR = "uploads"
CV_PARSER_DIR = "../Resume_Analyzer/CV_PARSER_MODEL"
RESULTS_DIR = "results"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

@app.post("/upload-cv")
async def upload_cv(file: UploadFile = File(...)):
    try:
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cv_{timestamp}.pdf"
        filepath = os.path.join(UPLOAD_DIR, filename)
        
        # Save uploaded file
        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {"filename": filename, "status": "success"}
        
    except Exception as e:
        return {"error": str(e), "status": "failed"}

@app.post("/analyze-cv")
async def analyze_cv(request: dict):
    try:
        filename = request.get("filename")
        if not filename:
            raise ValueError("Filename not provided")
            
        cv_path = os.path.join(UPLOAD_DIR, filename)
        if not os.path.exists(cv_path):
            raise FileNotFoundError("CV file not found")

        # Call CV parser
        parser_script = os.path.join(CV_PARSER_DIR, "main.py")
        result = subprocess.run([
            "python3",
            parser_script,
            "parse_cv",
            "--path", cv_path,
            "--save",
            "--console"
        ], capture_output=True, text=True)

        if result.returncode != 0:
            raise Exception(f"Parser failed: {result.stderr}")

        # Read parser results
        results_path = os.path.join(CV_PARSER_DIR, "results", 
                                  f"parsed_resume_{timestamp}.json")
        with open(results_path, 'r') as f:
            parser_results = json.load(f)

        # Extract relevant information
        analysis = {
            "skills": parser_results["parsers"]["custom"]["Skills"],
            "scores": parser_results["scores"]["custom"]["detailed_scores"],
            "recommendations": parser_results["skill_recommendations"]["recommendations"]
        }

        return analysis

    except Exception as e:
        return {"error": str(e), "status": "failed"}