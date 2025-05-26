#!/usr/bin/python3

# -*- coding: utf-8 -*-
# @Author  : Yasser JEMLI
# @File    : ResumeInfoExtractor.py
# @Description: Extracts structured information from resume paragraphs.

import re
import json
import os
from pathlib import Path

class ResumeInfoExtractor:
    def __init__(self, paragraphs):
        if not paragraphs:
            raise ValueError("No paragraphs provided")
            
        # Convert to list if string is passed
        if isinstance(paragraphs, str):
            self.paragraphs = [p for p in paragraphs.split('\n\n') if p.strip()]
        else:
            self.paragraphs = [p for p in paragraphs if p.strip()]
            
        if not self.paragraphs:
            raise ValueError("No valid paragraphs after processing")
            
        self.text = "\n".join(self.paragraphs)
        print(f"Debug: Loaded {len(self.paragraphs)} paragraphs")
        
        self.skills_file = Path(__file__).parent.parent / 'assets' / 'skills_keywords.json'
        self.experience_file = Path(__file__).parent.parent / 'assets' / 'experience_keywords.json'
        self.education_file = Path(__file__).parent.parent / 'assets' / 'education_keywords.json'
        self.skill_keywords = self._load_skills()
        self.experience_keywords = self._load_experience_keywords()
        self.education_keywords = self._load_education_keywords()
        print(f"Debug: Loaded {len(self.skill_keywords)} skills")

    def _load_skills(self):
        """Load skills from JSON file"""
        try:
            with open(self.skills_file, 'r') as f:
                skills_data = json.load(f)
                # Flatten the dictionary of skill categories into a single list
                return [skill.lower() for category in skills_data.values() for skill in category]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading skills file: {e}")
            return []

    def _load_experience_keywords(self):
        """Load experience keywords from JSON file"""
        try:
            with open(self.experience_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading experience keywords: {str(e)}")
            return {
                "section_headers": [],
                "date_patterns": [],
                "position_indicators": [],
                "company_indicators": [],
                "action_verbs": []
            }

    def _load_education_keywords(self):
        """Load education keywords from JSON file"""
        try:
            with open(self.education_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading education keywords: {str(e)}")
            return {
                "section_headers": [],
                "degree_types": {},
                "fields": [],
                "institutions": []
            }

    def extract_name(self):
        # Naive assumption: first non-empty line is the name
        for line in self.text.splitlines():
            if line.strip() and not any(char.isdigit() for char in line):
                return line.strip()
        return "Name not found"

    def extract_emails(self):
        return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", self.text)

    def extract_phone_numbers(self):
        """Extract phone numbers with improved validation"""
        phone_patterns = [
            # International format with country code
            r'(?:\+\d{1,3}[-\s]?)?\d{8,12}',
            # Format: +XXX XXXXXXXX
            r'\+\d{1,3}\s\d{8}',
            # Common Tunisian format
            r'\+216\s\d{8}'
        ]
        
        found_numbers = []
        
        for para in self.paragraphs:
            for pattern in phone_patterns:
                matches = re.finditer(pattern, para)
                for match in matches:
                    number = match.group().strip()
                    # Additional validation
                    if self._is_valid_phone(number):
                        found_numbers.append(number)
        
        # Remove duplicates while maintaining order
        unique_numbers = list(dict.fromkeys(found_numbers))
        
        return unique_numbers if unique_numbers else ["No phone number found"]

    def _is_valid_phone(self, number):
        """Validate phone number"""
        # Remove all non-digit characters except '+'
        cleaned = ''.join(c for c in number if c.isdigit() or c == '+')
        
        # Basic validation rules
        if not cleaned:
            return False
            
        # Must start with + or digit
        if not (cleaned.startswith('+') or cleaned[0].isdigit()):
            return False
            
        # Check length (including country code)
        if len(cleaned) < 8 or len(cleaned) > 15:
            return False
            
        # If starts with +, must have proper country code
        if cleaned.startswith('+'):
            # For Tunisia (+216)
            if cleaned.startswith('+216'):
                return len(cleaned) == 12  # +216 + 8 digits
                
        # Must contain only digits after potential '+'
        if not cleaned[1:].isdigit():
            return False
            
        # Reject if contains year-like numbers
        if re.search(r'[12]\d{3}', cleaned):
            return False
            
        return True

    def extract_skills(self):
        """Extract skills from resume text using loaded keywords"""
        found_skills = []
        for skill in self.skill_keywords:
            if re.search(r'\b' + re.escape(skill) + r'\b', self.text.lower()):
                found_skills.append(skill)
        return found_skills

    def extract_experience(self):
        """Extract work experience using keywords from JSON file"""
        experience_sections = []
        current_section = []
        in_experience_section = False
        
        lines = self.text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Check section headers
            if any(header.lower() in line.lower() 
                   for header in self.experience_keywords['section_headers']):
                in_experience_section = True
                if current_section:
                    experience_sections.append(' '.join(current_section))
                    current_section = []
                continue
                
            # Identify experience entries using position and company indicators
            has_position = any(indicator.lower() in line.lower() 
                             for indicator in self.experience_keywords['position_indicators'])
            has_company = any(indicator.lower() in line.lower() 
                             for indicator in self.experience_keywords['company_indicators'])
            
            if in_experience_section and (has_position or has_company):
                if current_section:
                    experience_sections.append(' '.join(current_section))
                current_section = [line]
                continue
                
            if in_experience_section:
                current_section.append(line)
        
        # Add final section
        if current_section:
            experience_sections.append(' '.join(current_section))
        
        # Clean and format sections
        cleaned_sections = []
        for section in experience_sections:
            cleaned = ' '.join(section.split())
            cleaned = re.sub(r'---\s*Paragraph\s*\d+\s*---', '', cleaned)
            if cleaned:
                cleaned_sections.append(cleaned)
        
        return cleaned_sections if cleaned_sections else ["No experience found"]

    def extract_education(self):
        """Extract education information with improved pattern matching"""
        education = {
            "total_institutions": 0,
            "institutions": [],
            "entries": []
        }
        
        # Get education section text
        edu_text = self._get_education_section()
        if not edu_text:
            return education

        # Track processed institutions to avoid duplicates
        processed = {}
        
        # Process each paragraph
        paragraphs = [p.strip() for p in edu_text.split('\n') if p.strip()]
        
        # Process each paragraph with a 2-paragraph lookahead for context
        for i in range(len(paragraphs)):
            context = ' '.join(paragraphs[i:i+3])
            
            for level, level_data in self.education_keywords["education_levels"].items():
                for inst_name, inst_data in level_data["institutions"].items():
                    if self._matches_institution(context, inst_data["keywords"]):
                        if inst_name in processed:
                            continue
                        entry = {
                            "institution": inst_data["name"],
                            "type": inst_data["type"],
                            "category": level,
                            "degree": self._match_degree(context, inst_data["degrees"]),
                            "period": self._match_date(context)
                        }
                        processed[inst_name] = entry
                        if inst_data["name"] not in education["institutions"]:
                            education["institutions"].append(inst_data["name"])

        
        education["entries"] = list(processed.values())
        education["total_institutions"] = len(education["institutions"])
        return education

    def _get_education_section(self):
        """Extract education section text"""
        text = ' '.join(self.paragraphs)
        start_idx = -1
        
        # Find start marker
        for marker in self.education_keywords["section_markers"]["start"]:
            idx = text.lower().find(marker.lower())
            if idx != -1 and (start_idx == -1 or idx < start_idx):
                start_idx = idx
        
        if start_idx == -1:
            return None
        
        # Find end marker
        end_idx = len(text)
        for marker in self.education_keywords["section_markers"]["end"]:
            idx = text.lower().find(marker.lower(), start_idx)
            if idx != -1 and idx < end_idx:
                end_idx = idx
        
        return text[start_idx:end_idx].strip()

    def _matches_institution(self, text, keywords):
        """Check if text matches institution keywords"""
        text_lower = text.lower()
        return any(keyword.lower() in text_lower for keyword in keywords)

    def _match_degree(self, text, degrees):
        """Match degree from text using degree keywords"""
        text_lower = text.lower()
        for degree in degrees:
            if all(keyword.lower() in text_lower for keyword in degree["keywords"]):
                return degree["name"]
        return None

    def _match_date(self, text):
        """Extract date or date range from text"""
        patterns = [
            r'\b(19|20)\d{2}\s*[-to]{1,3}\s*(19|20)\d{2}\b',  # 2010-2014 or 2010 to 2014
            r'\b(19|20)\d{2}\b',                              # Single year
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s*(19|20)\d{2}',  # Month Year
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group()
        return None

    def extract_all(self):
        """Extract all information from the resume"""
        try:
            results = {
                "Name": self.extract_name(),
                "Email": self.extract_emails(),
                "Phone": self.extract_phone_numbers(),
                "Skills": self.extract_skills(),
                "Experience": self.extract_experience(),
                "Education": self.extract_education()
            }
            print("Debug: Extraction complete")
            return results
        except Exception as e:
            print(f"Error in extract_all: {str(e)}")
            return None
