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
import logging
from pathlib import Path
from datetime import datetime
import json

from utilis.watchdog import Watchdog
from parsers.PDFTextExtractorPyMuPDF import PDFTextExtractorPyMuPDF
from parsers.PDFTextExtractorPdfMiner import PDFTextExtractorPdfMiner
from parsers.ResumeInfoExtractor import ResumeInfoExtractor
import sys
sys.path.append(str(Path(__file__).parent / 'parsers'))
try:
    try:
        from parsers.PyResParserExtractor import PyResParserExtractor
        HAS_PYRESPARSER = True
    except ModuleNotFoundError:
        print("[ERROR] Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
        HAS_PYRESPARSER = False
except ModuleNotFoundError:
    print("[ERROR] Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
    HAS_PYRESPARSER = False
# from utilis.logger import ResumeParserLogger

TEMP_FILE = "temp_save.txt"

HELP_TEXT = """
Resume Analyzer CLI

Usage:
    python main.py <action> --path <file_path> [--timeout <seconds>]

Actions:
    parse_cv     Parse the resume/CV and extract paragraphs
    recommend    Recommend courses based on the resume
    match        Match resume to job offers
    compare      Compare parsers for resume extraction

Examples:
    python main.py parse_cv --path resume.pdf
    python main.py recommend --path resume.pdf --timeout 15
    python main.py compare --path resume.pdf
"""

def setup_logging():
    log_file = Path(__file__).parent / 'logs' / 'parser_comparison.log'
    log_file.parent.mkdir(exist_ok=True)
    
    logging.basicConfig(
        filename=str(log_file),
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger('ParserComparison')

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

def extract_pdf_text_using_PdfMuPDF(pdf_path):
    try:
        extractor = PDFTextExtractorPyMuPDF(pdf_path)
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

        print("\n\n")
        print("================================= Using PDF MINER ================================")
        print(f"[DEBUG] Extracted {len(paragraphs)} paragraphs")
        print("==================================================================================")
        print(paragraphs)
        print("===============================================================================")
        
        # Create formatted output with non-empty paragraphs
        output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" 
                             for i, para in enumerate(paragraphs) 
                             if para.strip()])
        return output if output else None

    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDF: {str(e)}")
        return None
    
def extract_pdf_text_using_PdfMiner(pdf_path):
    try:
        extractor = PDFTextExtractorPdfMiner(pdf_path)
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
        print("\n\n")
        print("================================= Using PDF MINER ================================")
        print(f"[DEBUG] Extracted {len(paragraphs)} paragraphs")
        print("==================================================================================")
        print(paragraphs)
        print("===============================================================================")
        
        # Create formatted output with non-empty paragraphs
        output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" 
                             for i, para in enumerate(paragraphs) 
                             if para.strip()])
        return output if output else None

    except Exception as e:
        print(f"[ERROR] Failed to extract text from PDF: {str(e)}")
        return None

def print_parser_results(results):
    """Pretty print parser results"""
    if not results:
        print("No results available")
        return
        
    for key, value in results.items():
        print(f"\n{key}:")
        if isinstance(value, list):
            for item in value:
                print(f"- {item}")
        else:
            print(value)

def compare_parsers(pdf_path):
    """Compare results from different parser implementations"""
    logger = logging.getLogger('ParserComparison')
    results = {}
    
    try:
        # 1. Extract text using PdfMiner (preferred method)
        logger.info("Extracting text using PdfMiner...")
        miner_text = extract_pdf_text_using_PdfMiner(pdf_path)
        
        if not miner_text:
            # Fallback to PyMuPDF if PdfMiner fails
            logger.warning("PdfMiner failed, falling back to PyMuPDF...")
            miner_text = extract_pdf_text_using_PdfMuPDF(pdf_path)
        
        if not miner_text:
            logger.error("Failed to extract text from PDF")
            return False
            
        # 2. Parse with ResumeInfoExtractor
        logger.info("Parsing with ResumeInfoExtractor...")
        custom_parser = ResumeInfoExtractor(miner_text)
        results['custom'] = custom_parser.extract_all()
        
        # 3. Parse with PyResParser if available
        if HAS_PYRESPARSER:
            logger.info("Parsing with PyResParser...")
            py_parser = PyResParserExtractor(pdf_path)
            results['pyres'] = py_parser.extract_all()
        
        # 4. Print comparison results
        print("\n=== Parsing Results Comparison ===\n")
        
        for field in ['Name', 'Email', 'Phone', 'Skills', 'Experience']:
            print(f"\n{field}:")
            print("-" * 40)
            
            # Custom parser results
            print("ResumeInfoExtractor:")
            value = results['custom'].get(field, [])
            if isinstance(value, list):
                for item in value:
                    print(f"  - {item}")
            else:
                print(f"  {value}")
                
            # PyResParser results if available
            if HAS_PYRESPARSER:
                print("\nPyResParser:")
                value = results['pyres'].get(field, [])
                if isinstance(value, list):
                    for item in value:
                        print(f"  - {item}")
                else:
                    print(f"  {value}")
            
            print()
        
        return results
        
    except Exception as e:
        logger.error(f"Parser comparison failed: {str(e)}")
        raise

def CV_parsing_main(pdf_path, save_results=False):
    """Main parsing function with optional result saving"""
    try:
        # Set up logging with console handler
        logger = logging.getLogger('ResumeParser')
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        logger.info(f"Processing PDF: {pdf_path}")
        
        # Run parsers and get results
        results = compare_parsers(pdf_path)
        
        if results:
            logger.info("Successfully parsed resume")
            
            # Save results if flag is set
            if save_results:
                output_dir = Path(__file__).parent / 'results'
                output_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = output_dir / f'parsed_resume_{timestamp}.json'
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)
                logger.info(f"Results saved to: {output_file}")
                
            return results
        else:
            logger.error("Failed to parse resume")
            return None
            
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument('action', choices=['parse_cv', 'recommend', 'match', 'compare'])
    parser.add_argument('--path', required=True, help='Path to the resume PDF file')
    parser.add_argument('--save', action='store_true', help='Save results to JSON file')
    args = parser.parse_args()
    
    if args.action == 'parse_cv':
        CV_parsing_main(args.path, save_results=args.save)