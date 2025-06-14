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
import time

from utilis.watchdog import Watchdog
from utilis.log_manager import LogManager
from parsers.PDFTextExtractorPyMuPDF import PDFTextExtractorPyMuPDF
from parsers.PDFTextExtractorPdfMiner import PDFTextExtractorPdfMiner
from parsers.ResumeInfoExtractor import ResumeInfoExtractor
from parsers.cv_scorer import CVScorer
from recommanders.skill_recommander import SkillRecommender
from recommanders.course_recommander import CourseRecommender
import sys
sys.path.append(str(Path(__file__).parent / 'parsers'))
logger_manager = LogManager.get_log_manager()
logger = logger_manager.get_logger(__name__)
try:
    logger.info("Trying to import PyResParserExtractor")
    try:
        from parsers.PyResParserExtractor import PyResParserExtractor
        HAS_PYRESPARSER = True
    except ModuleNotFoundError:
        logger.error("Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
        HAS_PYRESPARSER = False
except ModuleNotFoundError:
    logger.error("Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
    HAS_PYRESPARSER = False

# Initialize log manager
log_manager = LogManager.get_log_manager()
logger = log_manager.get_logger(__name__)

# Register cleanup
atexit.register(log_manager.shutdown)

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

# Handle Ctrl+C and SIGTERM
def handle_exit(signum, frame):
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
            logger.warning("No paragraphs extracted from PDF")
            return None

        logger.info(f"Extracted {len(paragraphs)} paragraphs from PDF")
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
        logger.error(f"Failed to extract text from PDF: {str(e)}")
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
            logger.warning("No paragraphs extracted from PDF")
            return None

        logger.info(f"Extracted {len(paragraphs)} paragraphs from PDF")
        logger.info(f"********************************************************")
        logger.info("******************** Printing paragraphs *****************")
        logger.info(paragraphs)
        logger.info(f"********************************************************")
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
        logger.error(f"Failed to extract text from PDF: {str(e)}")
        return None

def print_parser_results(results):
    """Pretty print parser results"""
    if not results:
        logger.error("No results available")
        return
        
    for key, value in results.items():
        print(f"\n{key}:")
        logger.info(f"{key}:")
        if isinstance(value, list):
            for item in value:
                logger.info(f"-{item}")
                print(f"- {item}")
        else:
            print(value)

def compare_parsers(pdf_path):
    """Compare results from different parser implementations"""
    logger = logging.getLogger('ParserComparison')
    results = {
        'extraction_methods': {},
        'parsers': {}
    }
    
    try:
        # 1. Extract text using both methods

        logger.info("Extracting text using PdfMiner...")
        miner_text = extract_pdf_text_using_PdfMiner(pdf_path)
        results['extraction_methods']['pdfminer'] = miner_text
        
        logger.info("Extracting text using PyMuPDF...")
        pymupdf_text = extract_pdf_text_using_PdfMuPDF(pdf_path)
        results['extraction_methods']['pymupdf'] = pymupdf_text
        
        # Use PdfMiner text as primary, fallback to PyMuPDF if needed
        text_to_parse = miner_text if miner_text else pymupdf_text
        
        if not text_to_parse:
            logger.error("Failed to extract text from PDF using both methods")
            return False
            
        # 2. Parse with ResumeInfoExtractor
        logger.info("Parsing with ResumeInfoExtractor...")
        custom_parser = ResumeInfoExtractor(text_to_parse)
        results['parsers']['custom'] = custom_parser.extract_all()
        
        # 3. Parse with PyResParser if available
        if HAS_PYRESPARSER:
            logger.info("Parsing with PyResParser...")
            py_parser = PyResParserExtractor(pdf_path)
            results['parsers']['pyres'] = py_parser.extract_all()
        
        # 4. Print comparison results
        print("\n=== Parsing Results Comparison ===\n")
        print_parser_results(results['parsers'])
        
        return results
        
    except Exception as e:
        logger.error(f"Parser comparison failed: {str(e)}")
        raise

def score_parsed_cv(parsed_results):
    """Score CV based on parsed results"""
    logger.info("Scoring CV...")
    scorer = CVScorer()
    
    scores = {}
    for parser_name, parser_data in parsed_results['parsers'].items():
        scores[parser_name] = scorer.score_cv(parser_data)
        
    return scores

def measure_execution_time(func):
    """Decorator to measure execution time of functions"""
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"\n{'='*20} Execution Time {'='*20}")
        print(f"Function '{func.__name__}' took {execution_time:.2f} seconds to execute")
        print('='*55)
        return result
    return wrapper

@measure_execution_time
def CV_parsing_main(pdf_path, save_results=False):
    try:
        logger.info(f"Processing PDF: {pdf_path}")
        results = compare_parsers(pdf_path)
        
        if results:
            # Add skill recommendations
            custom_results = results['parsers'].get('custom', {})
            current_skills = custom_results.get('Skills', [])
            position = custom_results.get('Position', 'sw_designer')  # default to sw_designer if not found
            
            # Get skill recommendations
            recommender = SkillRecommender()
            skill_recommendations = recommender.recommend_skills(position, current_skills)
            
            # Get course recommendations
            course_recommender = CourseRecommender()
            course_recommendations = course_recommender.recommend_courses(skill_recommendations)
            
            # Add recommendations to results
            results['skill_recommendations'] = skill_recommendations
            results['learning_path'] = course_recommendations
            
            # Score the CV
            cv_scores = score_parsed_cv(results)
            results['scores'] = cv_scores
            
            logger.info("Successfully parsed, scored and generated recommendations")
            
            if save_results:
                output_dir = Path(__file__).parent / 'results'
                output_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = output_dir / f'parsed_resume_{timestamp}.json'
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)
                logger.info(f"Results saved to: {output_file}")
            
            if args.console:
                print("\n=== CV Analysis Results ===")
                print(f"\nCurrent Position: {position}")
                print("\nSkill Recommendations:")
                if skill_recommendations["status"] == "success":
                    print("\nMissing Required Skills:")
                    for skill in skill_recommendations["recommendations"]["missing_required"]:
                        print(f"- {skill}")
                    
                    print("\nMissing Preferred Skills:")
                    for skill in skill_recommendations["recommendations"]["missing_preferred"]:
                        print(f"- {skill}")
                    
                    print("\nRelated Skills to Consider:")
                    for skill in skill_recommendations["recommendations"]["related_skills"]:
                        print(f"- {skill}")
                
                print("\n=== Learning Resources ===")
                if course_recommendations["status"] == "success":
                    print("\nPriority Courses:")
                    for skill, courses in course_recommendations["high_priority"].items():
                        print(f"\nFor {skill.upper()}:")
                        if courses["udemy"]:
                            print("  Udemy Courses:")
                            for course in courses["udemy"][:2]:
                                print(f"    - {course['title']}")
                        if courses["certificates"]:
                            print("  Recommended Certificates:")
                            for cert in courses["certificates"]:
                                print(f"    - {cert}")
            
            return results
        else:
            logger.error("Failed to parse resume")
            return None
            
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}")
        return None

def setup_logging(enable_file_logging=False, enable_console=False):
    """Configure logging based on flags"""
    logger_manager = LogManager.get_log_manager()
    
    # Configure logging levels and handlers
    if not enable_file_logging and not enable_console:
        # Disable all logging
        logging.getLogger().handlers = []
        return logger_manager
    
    # Set up logging with specified handlers
    logger_manager.configure_logging(
        file_logging=enable_file_logging,
        console_logging=enable_console
    )
    
    return logger_manager

if __name__ == "__main__":
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description=HELP_TEXT)
    parser.add_argument('action', choices=['parse_cv', 'recommend', 'match', 'compare'])
    parser.add_argument('--path', required=True, help='Path to the resume PDF file')
    parser.add_argument('--save', action='store_true', help='Save results to JSON file')
    parser.add_argument('--logging', action='store_true', help='Enable logging to file')
    parser.add_argument('--console', action='store_true', help='Enable console output')
    args = parser.parse_args()
    
    # Setup logging based on flags
    log_manager = setup_logging(
        enable_file_logging=args.logging,
        enable_console=args.console
    )
    logger = log_manager.get_logger(__name__)
    
    if args.action == 'parse_cv':
        result = CV_parsing_main(args.path, save_results=args.save)
    
    # Only show execution time if console output is enabled
    if args.console:
        total_time = time.time() - start_time
        print(f"\n{'='*20} Total Execution Time {'='*20}")
        print(f"Total script execution time: {total_time:.2f} seconds")
        print('='*60)