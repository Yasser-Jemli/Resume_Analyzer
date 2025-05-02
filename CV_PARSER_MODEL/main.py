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
from parsers.ResumeInfoExtractor import ResumeInfoExtractor


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
            os.remove(TEMP_FILE)
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
    extractor = PDFTextExtractor(pdf_path)
    paragraphs = extractor.extract_paragraphs(TEMP_FILE)
    extractor.close()

    output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" for i, para in enumerate(paragraphs)])
    return output or "No paragraphs found."

def CV_parsing_main(pdf_path):
    extarcted_paragraphs = extract_pdf_text(pdf_path)
    info_extractor = ResumeInfoExtractor(extarcted_paragraphs)
    results = info_extractor.extract_all()

    for key, value in results.items():
        print(f"\n--- {key} ---")
        print(value if not isinstance(value, list) else ", ".join(value))

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
