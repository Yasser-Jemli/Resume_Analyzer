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
            
            # Convert lists to proper format
            if isinstance(data.get('skills', []), list):
                skills = {
                    "programming": [],
                    "tools": [],
                    "frameworks": [],
                    "platforms": [],
                    "other": data.get('skills', [])  # Put all skills in 'other' category
                }
            else:
                skills = data.get('skills', {"other": []})

            # Format experience data
            experience = []
            if isinstance(data.get('experience', []), list):
                for exp in data.get('experience', []):
                    if isinstance(exp, str):
                        experience.append({
                            "company": "Unknown",
                            "position": exp,
                            "period": "",
                            "responsibilities": []
                        })
                    elif isinstance(exp, dict):
                        experience.append(exp)

            results = {
                "Name": data.get('name', ''),
                "Email": data.get('email', ''),
                "Phone": data.get('mobile_number', ''),
                "Skills": skills,
                "Experience": experience if experience else [{"company": "Unknown", "position": "No experience found", "period": "", "responsibilities": []}],
                "Education": data.get('education', []),
                "Position": data.get('designation', 'sw_designer')
            }
            
            self.logger.debug(f"PyResParser results: {results}")
            return results
            
        except Exception as e:
            self.logger.error(f"PyResParser extraction error: {str(e)}")
            return {
                "Name": "",
                "Email": "",
                "Phone": "",
                "Skills": {"other": []},
                "Experience": [{"company": "Unknown", "position": "Error extracting experience", "period": "", "responsibilities": []}],
                "Education": [],
                "Position": "sw_designer"
            }