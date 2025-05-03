#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : main.py
# @Software: Vscode
# @Description: CLI interface for the Resume Analyzer.
# @License : MIT License

import argparse
import os
import atexit
import signal
import sys

from utilis.watchdog import Watchdog
from parsers.PDFTextExtractor import PDFTextExtractor
from parsers.ResumeInfoExtractor import *

TEMP_FILE = "temp_save.txt"

HELP_TEXT = """
Resume Analyzer CLI

Usage:
    python main.py <action> --path <file_path> [--timeout <seconds>]

Actions:
    parse_cv     Parse the resume/CV and extract paragraphs
    recommend    Recommend courses based on the resume
    match        Match resume to job offers

Examples:
    python main.py parse_cv --path resume.pdf
    python main.py recommend --path resume.pdf --timeout 15
"""

def cleanup_temp_file():
    if os.path.exists(TEMP_FILE):
        try:
            #os.remove(TEMP_FILE)
            print(f"[INFO] Deleted temporary file: {TEMP_FILE}")
        except Exception as e:
            print(f"[WARNING] Could not delete {TEMP_FILE}: {e}")

# Register cleanup for normal exit
atexit.register(cleanup_temp_file)

# Handle Ctrl+C and SIGTERM
def handle_exit(signum, frame):
    cleanup_temp_file()
    sys.exit(0)

signal.signal(signal.SIGINT, handle_exit)
signal.signal(signal.SIGTERM, handle_exit)

def extract_pdf_text(pdf_path):
    try:
        extractor = PDFTextExtractor(pdf_path)
        paragraphs = extractor.extract_paragraphs(TEMP_FILE)
        extractor.close()

        if not paragraphs:
            # Read from temp file as backup
            with open(TEMP_FILE, 'r', encoding='utf-8') as f:
                content = f.read()
                paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

        if not paragraphs:
            print("[WARNING] No paragraphs extracted from PDF")
            return None

        print(f"[DEBUG] Extracted {len(paragraphs)} paragraphs")
        
        # Create formatted output with non-empty paragraphs
        output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" 
                             for i, para in enumerate(paragraphs) 
                             if para.strip()])
        return output if output else None

    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDF: {str(e)}")
        return None

def CV_parsing_main(pdf_path):
    try:
        extracted_text = extract_pdf_text(pdf_path)
        if not extracted_text:
            print("[ERROR] No text could be extracted from the PDF")
            return None
        
        print(f"[DEBUG] Raw extracted text length: {len(extracted_text)}")
        
        # Clean the text by removing paragraph markers
        paragraphs = []
        for line in extracted_text.split('\n'):
            if not line.startswith('---'):
                paragraphs.append(line.strip())
        
        cleaned_text = '\n'.join(p for p in paragraphs if p)
        
        if not cleaned_text:
            print("[ERROR] No valid text content after cleaning")
            return None
            
        print(f"[DEBUG] Cleaned text length: {len(cleaned_text)}")
        
        # Initialize extractor and process text
        info_extractor = ResumeInfoExtractor(cleaned_text)
        results = info_extractor.extract_all()
        
        if results:
            print("\nExtracted Information:")
            print("=====================")
            for key, value in results.items():
                print(f"\n{key}:")
                if isinstance(value, list):
                    if value:
                        for item in value:
                            print(f"- {item}")
                    else:
                        print("None found")
                else:
                    print(value if value else "None found")
        
        return results
                
    except Exception as e:
        print(f"[ERROR] Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    parser = argparse.ArgumentParser(description="Resume Analyzer CLI", add_help=False)
    parser.add_argument("action", nargs="?", choices=["parse_cv", "recommend", "match"], help="Action to perform")
    parser.add_argument("--path", help="Path to CV or job file")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout in seconds for the process")
    parser.add_argument("-h", "--help", action="store_true", help="Show help menu")

    args = parser.parse_args()

    if args.help or not args.action or not args.path:
        print(HELP_TEXT)
        return

    actions = {
        "parse_cv": CV_parsing_main,
        # "recommend": recommend_courses,
        # "match": match_job
    }

    task_function = actions.get(args.action)
    if not task_function:
        print(f"Action '{args.action}' is not implemented yet.")
        return

    watchdog = Watchdog(target=task_function, args=(args.path,), timeout=args.timeout)
    result = watchdog.start()
    print(result)

if __name__ == "__main__":
    main()
