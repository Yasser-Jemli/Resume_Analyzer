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
from typing import Dict

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
    """Extract text using PdfMiner with proper resource management"""
    logger = logging.getLogger('PdfMiner')
    
    try:
        with PDFTextExtractorPdfMiner(pdf_path) as extractor:
            paragraphs = extractor.extract_paragraphs()
            if not paragraphs:
                logger.error("No text extracted from PDF")
                return None
            return '\n\n'.join(paragraphs)
    except Exception as e:
        logger.error(f"Failed to extract text from PDF: {e}")
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
    """Compare results from different parsers with improved accuracy"""
    logger = logging.getLogger('ParserComparison')
    results = {
        'extraction_methods': {},
        'parsers': {}
    }
    
    try:
        # Extract text using PDFMiner
        logger.info("Extracting text using PdfMiner...")
        miner_extractor = PDFTextExtractorPdfMiner(pdf_path)
        miner_paragraphs = miner_extractor.extract_paragraphs(add_markers=True)
        results['extraction_methods']['pdfminer'] = '\n'.join(miner_paragraphs)
        
        # Extract text using PyMuPDF
        logger.info("Extracting text using PyMuPDF...")
        pymupdf_extractor = PDFTextExtractorPyMuPDF(pdf_path)
        pymupdf_text = pymupdf_extractor.extract_text()
        results['extraction_methods']['pymupdf'] = pymupdf_text
        
        # Parse with ResumeInfoExtractor using PDFMiner text
        logger.info("Parsing with ResumeInfoExtractor...")
        custom_parser = ResumeInfoExtractor('\n'.join(miner_paragraphs))
        custom_results = custom_parser.extract_all()
        
        if custom_results:
            results['parsers']['custom'] = custom_results
            logger.info("Successfully parsed with ResumeInfoExtractor")
        
        # Parse with PyResParser
        if HAS_PYRESPARSER:
            logger.info("Parsing with PyResParser...")
            pyres_parser = PyResParserExtractor(pdf_path)
            pyres_results = pyres_parser.extract_all()
            if pyres_results:
                results['parsers']['pyres'] = pyres_results
        
        return results
        
    except Exception as e:
        logger.error(f"Parser comparison failed: {e}")
        return None

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

def parse_cv(pdf_path: str, save_results: bool = False) -> Dict:
    try:
        # Extract text using PDFMiner
        pdf_extractor = PDFTextExtractorPdfMiner(pdf_path)
        paragraphs = pdf_extractor.extract_paragraphs()

        # Parse using custom parser
        custom_parser = CustomParser()
        custom_results = custom_parser.parse(paragraphs)

        # Score the resume
        scorer = ResumeScorer()
        scores = scorer.score_resume(custom_results)

        results = {
            "parsers": {
                "custom": custom_results
            },
            "scores": {
                "custom": scores
            }
        }

        if save_results:
            save_results_to_json(results)

        return results

    except Exception as e:
        logger.error(f"Error in parse_cv: {e}")
        return {}

@measure_execution_time
def CV_parsing_main(pdf_path, save_results=False):
    try:
        logger.info(f"Processing PDF: {pdf_path}")
        results = compare_parsers(pdf_path)
        
        if not results or not isinstance(results, dict):
            logger.error("Invalid results from compare_parsers")
            return None
            
        # Validate parser results exist
        if 'parsers' not in results:
            logger.error("No parser results found")
            return None
            
        # Get the custom parser results (ResumeInfoExtractor)
        custom_results = results['parsers'].get('custom')
        if not custom_results:
            logger.error("No custom parser results found")
            return None
            
        # Extract skills and position with defaults
        current_skills = custom_results.get('Skills', [])
        if not isinstance(current_skills, list):
            current_skills = []
        position = custom_results.get('Position', 'sw_designer')
        
        # Get skill recommendations
        try:
            recommender = SkillRecommender()
            skill_recommendations = recommender.recommend_skills(position, current_skills)
            if not skill_recommendations:
                logger.warning("No skill recommendations generated")
                skill_recommendations = {"status": "error", "message": "No recommendations generated"}
        except Exception as e:
            logger.error(f"Error generating skill recommendations: {e}")
            skill_recommendations = {"status": "error", "message": str(e)}
        
        # Get course recommendations
        try:
            course_recommender = CourseRecommender()
            course_recommendations = course_recommender.recommend_courses(skill_recommendations)
            if not course_recommendations:
                logger.warning("No course recommendations generated")
                course_recommendations = {"status": "error", "message": "No recommendations generated"}
        except Exception as e:
            logger.error(f"Error generating course recommendations: {e}")
            course_recommendations = {"status": "error", "message": str(e)}
        
        # Add recommendations to results
        results['skill_recommendations'] = skill_recommendations
        results['learning_path'] = course_recommendations
        
        # Score the CV using the existing CVScorer
        try:
            cv_scorer = CVScorer()
            cv_scores = {
                'custom': cv_scorer.score_cv(custom_results) or {},
                'pyres': cv_scorer.score_cv(results['parsers'].get('pyres', {})) or {}
            }
            results['scores'] = cv_scores
        except Exception as e:
            logger.error(f"Error scoring CV: {e}")
            results['scores'] = {'error': str(e)}
        
        logger.info("Successfully parsed, scored and generated recommendations")
        
        if save_results:
            try:
                output_dir = Path(__file__).parent / 'results'
                output_dir.mkdir(exist_ok=True)
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                output_file = output_dir / f'parsed_resume_{timestamp}.json'
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=4, ensure_ascii=False)
                logger.info(f"Results saved to: {output_file}")
            except Exception as e:
                logger.error(f"Error saving results: {e}")
        
        if args.console:
            print("\n=== CV Analysis Results ===")
            print(f"\nCurrent Position: {position}")
            
            # Print scores safely
            if 'scores' in results:
                print("\nScores:")
                for parser_name, score in results['scores'].items():
                    if isinstance(score, dict) and 'total_score' in score:
                        print(f"\n{parser_name.upper()} Parser Score:")
                        print(f"Total Score: {score['total_score']:.1f}")
                        if 'detailed_scores' in score:
                            print("Detailed Scores:")
                            for category, cat_score in score['detailed_scores'].items():
                                print(f"- {category}: {cat_score:.1f}")
            
            # Print recommendations safely
            if skill_recommendations.get("status") == "success":
                print("\nSkill Recommendations:")
                recommendations = skill_recommendations.get("recommendations", {})
                
                if "missing_required" in recommendations:
                    print("\nMissing Required Skills:")
                    for skill in recommendations["missing_required"]:
                        print(f"- {skill}")
                
                if "missing_preferred" in recommendations:
                    print("\nMissing Preferred Skills:")
                    for skill in recommendations["missing_preferred"]:
                        print(f"- {skill}")
                
                if "related_skills" in recommendations:
                    print("\nRelated Skills to Consider:")
                    for skill in recommendations["related_skills"]:
                        print(f"- {skill}")
        
        return results
            
    except Exception as e:
        logger.error(f"Exception occurred: {str(e)}", exc_info=True)
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