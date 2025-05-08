#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : main.py
# @Software: Vscode
# @Description: CLI interface for the Resume Analyzer.
# @License : MIT License

# import argparse
# import os
# import atexit
# import signal
# import sys
# import logging
# from pathlib import Path

# from utilis.watchdog import Watchdog
# from parsers.PDFTextExtractorPyMuPDF import PDFTextExtractorPyMuPDF
# from parsers.PDFTextExtractorPdfMiner import PDFTextExtractorPdfMiner
# from parsers.ResumeInfoExtractor import ResumeInfoExtractor
# import sys
# sys.path.append(str(Path(__file__).parent / 'parsers'))
# try:
#     try:
#         from parsers.PyResParserExtractor import PyResParserExtractor
#         HAS_PYRESPARSER = True
#     except ModuleNotFoundError:
#         print("[ERROR] Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
#         HAS_PYRESPARSER = False
# except ModuleNotFoundError:
#     print("[ERROR] Could not import 'PyResParserExtractor'. Ensure the 'parsers' directory is in the Python path and contains 'PyResParserExtractor.py'.")
#     HAS_PYRESPARSER = False
# # from utilis.logger import ResumeParserLogger

# TEMP_FILE = "temp_save.txt"

# HELP_TEXT = """
# Resume Analyzer CLI

# Usage:
#     python main.py <action> --path <file_path> [--timeout <seconds>]

# Actions:
#     parse_cv     Parse the resume/CV and extract paragraphs
#     recommend    Recommend courses based on the resume
#     match        Match resume to job offers
#     compare      Compare parsers for resume extraction

# Examples:
#     python main.py parse_cv --path resume.pdf
#     python main.py recommend --path resume.pdf --timeout 15
#     python main.py compare --path resume.pdf
# """

# def setup_logging():
#     log_file = Path(__file__).parent / 'logs' / 'parser_comparison.log'
#     log_file.parent.mkdir(exist_ok=True)
    
#     logging.basicConfig(
#         filename=str(log_file),
#         level=logging.DEBUG,
#         format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
#     )
#     return logging.getLogger('ParserComparison')

# def cleanup_temp_file():
#     if os.path.exists(TEMP_FILE):
#         try:
#             #os.remove(TEMP_FILE)
#             print(f"[INFO] Deleted temporary file: {TEMP_FILE}")
#         except Exception as e:
#             print(f"[WARNING] Could not delete {TEMP_FILE}: {e}")

# # Register cleanup for normal exit
# atexit.register(cleanup_temp_file)

# # Handle Ctrl+C and SIGTERM
# def handle_exit(signum, frame):
#     cleanup_temp_file()
#     sys.exit(0)

# signal.signal(signal.SIGINT, handle_exit)
# signal.signal(signal.SIGTERM, handle_exit)

# def extract_pdf_text_using_PdfMuPDF(pdf_path):
#     try:
#         extractor = PDFTextExtractorPyMuPDF(pdf_path)
#         paragraphs = extractor.extract_paragraphs(TEMP_FILE)
#         extractor.close()

#         if not paragraphs:
#             # Read from temp file as backup
#             with open(TEMP_FILE, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

#         if not paragraphs:
#             print("[WARNING] No paragraphs extracted from PDF")
#             return None

#         print(f"[DEBUG] Extracted {len(paragraphs)} paragraphs")
#         print("==================================================================================")
#         print(paragraphs)
#         print("===============================================================================")
        
#         # Create formatted output with non-empty paragraphs
#         output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" 
#                              for i, para in enumerate(paragraphs) 
#                              if para.strip()])
#         return output if output else None

#     except Exception as e:
#         print(f"[ERROR] Failed to extract text from PDF: {str(e)}")
#         return None
    
# def extract_pdf_text_using_PdfMiner(pdf_path):
#     try:
#         extractor = PDFTextExtractorPdfMiner(pdf_path)
#         paragraphs = extractor.extract_paragraphs(TEMP_FILE)
#         extractor.close()

#         if not paragraphs:
#             # Read from temp file as backup
#             with open(TEMP_FILE, 'r', encoding='utf-8') as f:
#                 content = f.read()
#                 paragraphs = [p.strip() for p in content.split('\n') if p.strip()]

#         if not paragraphs:
#             print("[WARNING] No paragraphs extracted from PDF")
#             return None

#         print(f"[DEBUG] Extracted {len(paragraphs)} paragraphs")
#         print("==================================================================================")
#         print(paragraphs)
#         print("===============================================================================")
        
#         # Create formatted output with non-empty paragraphs
#         output = "\n\n".join([f"--- Paragraph {i+1} ---\n{para}" 
#                              for i, para in enumerate(paragraphs) 
#                              if para.strip()])
#         return output if output else None

#     except Exception as e:
#         print(f"[ERROR] Failed to extract text from PDF: {str(e)}")
#         return None

# def print_parser_results(results):
#     """Pretty print parser results"""
#     if not results:
#         print("No results available")
#         return
        
#     for key, value in results.items():
#         print(f"\n{key}:")
#         if isinstance(value, list):
#             for item in value:
#                 print(f"- {item}")
#         else:
#             print(value)

# def compare_parsers(pdf_path):
#     """Compare results from both parsers"""
#     logger = logging.getLogger('ParserComparison')
    
#     try:
#         # Custom parser extraction
#         logger.info("Running custom parser...")
#         extracted_text = extract_pdf_text_using_PdfMuPDF(pdf_path)
#         extracted_text1 = extract_pdf_text_using_PdfMiner(pdf_path)
#         custom_parser = ResumeInfoExtractor(extracted_text)
#         custom_parser1 = ResumeInfoExtractor(extracted_text1)

#         custom_results = custom_parser.extract_all()
#         custom_results1 = custom_parser1.extract_all()
        
#         print("=========================================================================================")
#         print("\nCustom Parser Results (using PyMuPDF):")
#         print("=========================================================================================")
#         print_parser_results(custom_results)

#         print("=========================================================================================")
#         print("\nCustom Parser Results (using PdfMiner):")
#         print("=========================================================================================")
#         print_parser_results(custom_results1)
        
#         # PyResParser extraction (if available)
#         if HAS_PYRESPARSER:
#             logger.info("Running PyResParser...")
#             py_parser = PyResParserExtractor(pdf_path)
#             pyres_results = py_parser.extract_all()
            
#             print("=========================================================================================")
#             print("\nPyResParser Results:")
#             print("=========================================================================================")
#             print_parser_results(pyres_results)
#         else:
#             logger.warning("PyResParser not available - skipping comparison")

#         if HAS_PYRESPARSER:
#             logger.info("Comparing results...")
            
#             print("=========================================================================================")
#             print("\nComparison Results:")
#             print("=========================================================================================")
#             print_parser_results(comparison_results)
            
#     except Exception as e:
#         logger.error(f"Parser comparison failed: {str(e)}")
#         raise

# def CV_parsing_main(pdf_path):
#     """Main parsing function"""
#     try:
#         # Set up logging
#         logger = logging.getLogger('ResumeParser')
        
#         # Run both parsers
#         compare_parsers(pdf_path)
#         return True
        
#     except Exception as e:
#         print(f"[ERROR] Exception occurred: {str(e)}")
#         return False

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description=HELP_TEXT)
#     parser.add_argument('action', choices=['parse_cv', 'recommend', 'match', 'compare'])
#     parser.add_argument('--path', required=True, help='Path to the resume PDF file')
#     args = parser.parse_args()
    
#     if args.action == 'parse_cv':
#         CV_parsing_main(args.path)

from states.init_state import InitState
from states.listener_state import EventListenerState
from states.publisher_state import EventPublisherState
from states.logger_state import LoggerState
from states.verify_state import VerifyState
import logging
import time

logging.basicConfig(level=logging.INFO)

class MainModule:
    def start(self):
        logging.info("Main Module Started")

        if not InitState().run():
            self.stop("Init failed")
            return

        listener_proc = EventListenerState().run()
        publisher_success = EventPublisherState().run()
        logger_success = LoggerState().run()

        listener_proc.join()

        if VerifyState().run(publisher_success, logger_success):
            logging.info("In OK: Share to Main Model")
        else:
            logging.warning("In KO: Share to Main Model")

        while(1):
            print("Listening....")
            time.sleep(1)

        self.stop("Done")

    def stop(self, reason):
        logging.info(f"Stopping: {reason}")
        # Add cleanup here

if __name__ == "__main__":
    MainModule().start()