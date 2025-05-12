import pdfplumber
import docx
import spacy
import re
import json
from pathlib import Path
from typing import Dict, Optional

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from a PDF file using pdfplumber."""
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from PDF: {e}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from a Word document using python-docx."""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
    except Exception as e:
        raise ValueError(f"Error extracting text from DOCX: {e}")

def extract_text(file_path: str) -> str:
    """Extract text from a CV file (PDF or DOCX)."""
    file_ext = Path(file_path).suffix.lower()
    if file_ext == ".pdf":
        return extract_text_from_pdf(file_path)
    elif file_ext in [".docx", ".doc"]:
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Use PDF or DOCX.")

def parse_cv(text: str) -> Dict:
    """Parse CV text to extract structured information using spaCy."""
    # Load spaCy's English model
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    # Initialize output dictionary
    cv_data = {
        "name": "",
        "email": "",
        "phone": "",
        "education": [],
        "experience": [],
        "skills": []
    }

    # Extract entities
    for ent in doc.ents:
        if ent.label_ == "PERSON" and not cv_data["name"]:
            cv_data["name"] = ent.text
        elif ent.label_ == "ORG":
            # Could be part of education or experience
            pass

    # Extract email using regex
    email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    emails = re.findall(email_pattern, text)
    if emails:
        cv_data["email"] = emails[0]

    # Extract phone number using regex
    phone_pattern = r"\b(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b"
    phones = re.findall(phone_pattern, text)
    if phones:
        cv_data["phone"] = phones[0][0] if phones[0][0] else phones[0][1]

    # Rule-based section extraction
    lines = text.split("\n")
    current_section = None
    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Identify section headers
        if re.match(r"^(education|academic|qualОрганизацияifications)\b", line, re.IGNORECASE):
            current_section = "education"
            continue
        elif re.match(r"^(experience|work|employment)\b", line, re.IGNORECASE):
            current_section = "experience"
            continue
        elif re.match(r"^(skills|technical skills|competencies)\b", line, re.IGNORECASE):
            current_section = "skills"
            continue

        # Append to relevant section
        if current_section == "education" and line:
            cv_data["education"].append(line)
        elif current_section == "experience" and line:
            cv_data["experience"].append(line)
        elif current_section == "skills" and line:
            cv_data["skills"].append(line)

    return cv_data

def parse_cv_file(file_path: str) -> Dict:
    """Main function to parse a CV file and return structured data."""
    try:
        text = extract_text(file_path)
        cv_data = parse_cv(text)
        return cv_data
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    # Example usage
    cv_file = "/home/yjemli@actia.local/Downloads/CV_Yasser_Jamli.pdf"  # Replace with your CV file path
    result = parse_cv_file(cv_file)
    print(json.dumps(result, indent=2))