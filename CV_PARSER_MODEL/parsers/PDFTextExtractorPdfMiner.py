#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Time    : 2025/05/08
# @Author  : Yasser JEMLI
# @File    : PDFTextExtractorPdfMiner.py
# @Software: Vscode
# @Description: This module extracts text from each text box using pdfminer3.

import io
import json
import logging
from pathlib import Path
from typing import List, Dict
from pdfminer3.layout import LAParams, LTTextBox, LTTextContainer
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer3.converter import PDFPageAggregator, TextConverter
from pdfminer3.pdfparser import PDFSyntaxError, PDFParser
from pdfminer3.pdfdocument import PDFDocument, PDFTextExtractionNotAllowed

class PDFTextExtractorPdfMiner:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.paragraphs = []
        self.logger = logging.getLogger(__name__)
        self._load_keyword_data()
        self.device = None
        self.interpreter = None
        self.document = None

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup"""
        self.close()
        if exc_type:
            self.logger.error(f"Error during PDF processing: {exc_val}")
            return False
        return True

    def close(self):
        """Clean up resources"""
        try:
            if self.device:
                self.device.close()
            if hasattr(self, '_file'):
                self._file.close()
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")

    def _load_keyword_data(self):
        """Load keyword dictionaries from assets"""
        try:
            assets_dir = Path(__file__).parent.parent / 'assets'
            
            with open(assets_dir / 'skills_keywords.json', 'r') as f:
                self.skills_keywords = json.load(f)
            
            with open(assets_dir / 'education_keywords.json', 'r') as f:
                self.education_keywords = json.load(f)
                
            with open(assets_dir / 'experience_keywords.json', 'r') as f:
                self.experience_keywords = json.load(f)
                
        except Exception as e:
            self.logger.error(f"Error loading keyword data: {e}")
            raise

    def load_pdf(self):
        """Load and extract text from PDF with enhanced error handling"""
        self.paragraphs = []
        try:
            # Open file and create parser
            self._file = open(self.pdf_path, 'rb')
            parser = PDFParser(self._file)
            
            # Create document and check extractability
            self.document = PDFDocument(parser)
            if not self.document.is_extractable:
                raise PDFTextExtractionNotAllowed(
                    f"Text extraction not allowed for: {self.pdf_path}"
                )

            # Set up PDF processing
            rsrcmgr = PDFResourceManager()
            laparams = LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5
            )
            self.device = PDFPageAggregator(rsrcmgr, laparams=laparams)
            self.interpreter = PDFPageInterpreter(rsrcmgr, self.device)

            # Process each page
            for page_num, page in enumerate(PDFPage.create_pages(self.document), 1):
                self.interpreter.process_page(page)
                layout = self.device.get_result()
                page_text = []
                
                # Extract text from layout elements
                for element in layout:
                    if isinstance(element, (LTTextBox, LTTextContainer)):
                        text = element.get_text().strip()
                        if text:
                            page_text.append(text)
                
                if page_text:
                    self.paragraphs.extend(page_text)
                    
            self.logger.info(
                f"Successfully extracted {len(self.paragraphs)} text blocks from: {self.pdf_path}"
            )
            return True
            
        except PDFSyntaxError as e:
            self.logger.error(f"Invalid PDF format: {e}")
            return False
        except PDFTextExtractionNotAllowed as e:
            self.logger.error(f"Text extraction not allowed: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Error processing PDF: {e}")
            return False
        finally:
            self.close()

    def extract_structured_data(self) -> Dict:
        """Extract structured data using enhanced keywords"""
        self.load_pdf()
        
        return {
            'contact_info': self._extract_contact_info(),
            'education': self._extract_education(),
            'experience': self._extract_experience(),
            'skills': self._extract_skills(),
            'raw_paragraphs': self.paragraphs
        }

    def _extract_contact_info(self) -> Dict:
        """Extract contact information using regex patterns"""
        import re
        
        contact_info = {
            'email': None,
            'phone': None,
            'linkedin': None,
            'github': None
        }
        
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(?:\+\d{1,3}[-.\s]?)?\d{8,12}'
        
        for para in self.paragraphs:
            # Extract email
            if not contact_info['email']:
                email_match = re.search(email_pattern, para)
                if email_match:
                    contact_info['email'] = email_match.group()
            
            # Extract phone with validation
            if not contact_info['phone']:
                phone_match = re.search(phone_pattern, para)
                if phone_match and not re.search(r'[12]\d{3}', phone_match.group()):  # Exclude years
                    contact_info['phone'] = phone_match.group()
            
            # Extract social links
            para_lower = para.lower()
            if 'linkedin.com' in para_lower:
                contact_info['linkedin'] = para.strip()
            if 'github.com' in para_lower:
                contact_info['github'] = para.strip()
                
        return contact_info

    def _extract_education(self) -> List[Dict]:
        """Extract education information using enhanced keywords"""
        education_entries = []
        
        for para in self.paragraphs:
            para_lower = para.lower()
            
            # Check for education section headers
            if any(header.lower() in para_lower for header in self.education_keywords.get('section_headers', [])):
                entry = {
                    'degree': None,
                    'field': None,
                    'institution': None,
                    'date': None
                }
                
                # Extract degree type
                for degree_type, keywords in self.education_keywords.get('degree_types', {}).items():
                    if any(keyword.lower() in para_lower for keyword in keywords):
                        entry['degree'] = degree_type
                        break
                
                # Extract field of study
                for field in self.education_keywords.get('fields', []):
                    if field.lower() in para_lower:
                        entry['field'] = field
                        break
                        
                if entry['degree'] or entry['field']:
                    education_entries.append(entry)
                    
        return education_entries

    def _extract_skills(self) -> List[str]:
        """Extract skills using categorized keywords"""
        skills = set()
        
        for para in self.paragraphs:
            para_lower = para.lower()
            
            # Check all skill categories
            for category in self.skills_keywords.values():
                if isinstance(category, dict):
                    for subcategory in category.values():
                        if isinstance(subcategory, list):
                            skills.update(
                                skill for skill in subcategory 
                                if skill.lower() in para_lower
                            )
                        elif isinstance(subcategory, dict):
                            for subskills in subcategory.values():
                                if isinstance(subskills, list):
                                    skills.update(
                                        skill for skill in subskills 
                                        if skill.lower() in para_lower
                                    )
                                    
        return list(skills)

    def _extract_experience(self) -> List[Dict]:
        """Extract experience information using enhanced keywords"""
        experiences = []
        current_entry = None
        
        for para in self.paragraphs:
            para_lower = para.lower()
            
            # Check for new experience entry
            if any(indicator in para_lower for indicator in self.experience_keywords.get('position_indicators', [])):
                if current_entry:
                    experiences.append(current_entry)
                    
                current_entry = {
                    'title': None,
                    'company': None,
                    'period': None,
                    'responsibilities': []
                }
                
                # Extract position title
                for position in self.experience_keywords.get('position_indicators', []):
                    if position.lower() in para_lower:
                        current_entry['title'] = position
                        break
                        
                # Extract company name
                for company_ind in self.experience_keywords.get('company_indicators', []):
                    if company_ind in para_lower:
                        # Take the line containing company indicator
                        lines = para.split('\n')
                        for line in lines:
                            if company_ind in line.lower():
                                current_entry['company'] = line.strip()
                                break
            
            # Add responsibilities to current entry
            elif current_entry:
                for verb in self.experience_keywords.get('action_verbs', []):
                    if verb.lower() in para_lower:
                        current_entry['responsibilities'].append(para.strip())
                        break
                        
        if current_entry:
            experiences.append(current_entry)
            
        return experiences

    def save_extracted_paragraphs(self, output_path):
        """Save extracted paragraphs with structured format"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                structured_data = self.extract_structured_data()
                json.dump(structured_data, f, indent=4)
            self.logger.info(f"Extracted data saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save extracted data: {e}")

    def extract_paragraphs(self, add_markers=True):
        """Extract paragraphs with improved formatting"""
        paragraphs = []
        paragraph_num = 1
        
        try:
            rsrcmgr = PDFResourceManager()
            output = io.StringIO()
            laparams = LAParams(
                line_margin=0.5,
                word_margin=0.1,
                char_margin=2.0,
                boxes_flow=0.5
            )
            
            device = TextConverter(rsrcmgr, output, laparams=laparams)
            interpreter = PDFPageInterpreter(rsrcmgr, device)
            
            with open(self.pdf_path, 'rb') as fp:
                for page in PDFPage.get_pages(fp):
                    interpreter.process_page(page)
                    
            text = output.getvalue()
            device.close()
            output.close()
            
            # Split into paragraphs and clean
            raw_paragraphs = text.split('\n\n')
            for para in raw_paragraphs:
                cleaned = para.strip()
                if cleaned:
                    if add_markers:
                        paragraphs.append(f"--- Paragraph {paragraph_num} ---\n{cleaned}")
                        paragraph_num += 1
                    else:
                        paragraphs.append(cleaned)
            
            return paragraphs
            
        except Exception as e:
            self.logger.error(f"Error extracting paragraphs: {e}")
            return []
