#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2023/10/12 16:00
# @Author  : Yasser JEMLI
# @File    : ResumeInfoExtractor.py
# @Description: Extracts structured information from resume paragraphs.

import logging
from pyresparser import ResumeParser
from pathlib import Path

class PyResParserExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.logger = logging.getLogger('PyResParser')

    def extract_all(self):
        try:
            self.logger.info(f"Starting pyresparser extraction for: {self.pdf_path}")
            data = ResumeParser(self.pdf_path).get_extracted_data()
            
            results = {
                "Name": data.get('name', ''),
                "Email": data.get('email', []),
                "Phone": data.get('mobile_number', []),
                "Skills": data.get('skills', []),
                "Experience": data.get('experience', ["No experience found"])
            }
            
            self.logger.debug(f"PyResParser results: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"PyResParser extraction error: {str(e)}")
            return None